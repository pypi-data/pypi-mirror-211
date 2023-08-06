"""
Find candidate duplex read pairs by examining sequencing summary.

This script takes a sequencing summary and examines:

 * The duration between strands (specifically the duration between the end of
   the current strand and start of next)
 * The proportion between the difference in length between these strands

"""
# TODO: rewrite this, its seems a little verbose/contorted
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import math
from pathlib import Path

import pandas as pd
import pysam
from tqdm import tqdm

import duplex_tools


def find_pairs(
        sequencing_summary_path: str,
        outdir: str = "1d2_pairs_noalign",
        prefix: str = "pair",
        prepend_seqsummary_stem: bool = False,
        max_time_between_reads=20,
        max_seqlen_diff=0.1,
        match_barcodes: bool = False,
        min_qscore: float = None,
        max_abs_seqlen_diff: int = None) -> None:
    """Find pairs using metrics stored in a sequencing summary file."""
    logger = duplex_tools.get_named_logger("FindPairs")
    logger.info(f'Duplex tools version: {duplex_tools.__version__}')
    outdir, output_pairs, output_intermediate = prepare_output_paths(
        outdir, prefix, prepend_seqsummary_stem, sequencing_summary_path)
    if Path(sequencing_summary_path).suffix in {'.bam', '.sam'}:
        logger.info('Creating seqsummary from bam')
        bamfile = pysam.AlignmentFile(sequencing_summary_path,
                                      check_sq=False)  # Allow uBAM
        records = []
        for read in tqdm(bamfile.fetch(until_eof=True)):  # Allow uBAM
            records.append({'read_id': read.qname,
                            'duration': read.get_tag('du'),
                            'start_time': read.get_tag('st'),
                            'channel': read.get_tag('ch'),
                            'mux': read.get_tag('mx'),
                            'sequence_length_template': read.query_length,
                            'mean_qscore_template': read.get_tag('qs')
                            }
                           )
        seqsummary = pd.DataFrame(records)
        seqsummary['start_time'] = (
                pd.to_datetime(seqsummary['start_time']) -
                pd.to_datetime(seqsummary['start_time']).min()
                ).dt.total_seconds().astype(float)
    else:
        logger.info('Loading sequencing summary.')
        dtype = {
            "read_id": str,
            "alignment_genome": str,
            "alignment_genome_start": pd.Int64Dtype(),
            "alignment_genome_end": pd.Int64Dtype(),
            "barcode_arrangement": str,
            "start_time": float,
            "duration": float,
            "channel": int, "mux": int,
            "sequence_length_template": int,
            "mean_qscore_template": float,
        }
        cols = set(dtype.keys())

        def take_column(x):
            return x in cols

        seqsummary = pd.read_csv(
            sequencing_summary_path, sep="\t",
            dtype=dtype, usecols=take_column,
            na_values={
                "alignment_genome_start": "-",
                "alignment_genome_end": "-"}
        )

    logger.info('Calculating metrics.')
    seqsummary = calculate_metrics_for_next_strand(seqsummary)

    try:
        seqsummary = calculate_alignment_metrics(seqsummary)
    except KeyError:
        logger.info("No alignment information found for validation.")

    logger.info('Classifying pairs.')
    tempcompsummary = seqsummary_to_tempcompsummary(
        seqsummary,
        max_time_between_reads=max_time_between_reads,
        max_seqlen_diff=max_seqlen_diff,
        match_barcodes=match_barcodes,
        min_qscore=min_qscore,
        max_abs_seqlen_diff=max_abs_seqlen_diff)

    candidate_pairs = seqsummary.query('candidate_followon')
    ncandidate_pairs = len(candidate_pairs)
    nstrands = len(seqsummary)
    frac_pairs = 100 * ncandidate_pairs * 2 / nstrands
    logger.info(
        f"Found {ncandidate_pairs} pairs within {nstrands} reads. "
        f"({frac_pairs:.1f}% of reads are part of a pair).")
    logger.info('Values above 100% are allowed since reads can be either '
                'template or complement')
    logger.info(f'Writing files into {outdir} directory')

    # Write
    tempcompsummary.to_csv(output_intermediate, index=False, sep="\t")
    candidate_pairs[['read_id', 'read_id_next']] \
        .drop_duplicates() \
        .to_csv(output_pairs, index=False, sep=" ", header=False)


def prepare_output_paths(
        outdir, prefix, prepend_seqsummary_stem, sequencing_summary_path):
    """Decide output paths."""
    sspath = Path(sequencing_summary_path)
    if prepend_seqsummary_stem:
        prefix = f"{sspath.stem}_{prefix}"
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    output_intermediate = Path(outdir, f'{prefix}_stats.txt')
    output_pairs = Path(outdir, f'{prefix}_ids.txt')
    return outdir, output_pairs, output_intermediate


def calculate_alignment_metrics(seqsummary) -> pd.DataFrame:
    """Calculate alignment metrics for validation.

    These are optional and are not used for classification.
    """
    seqsummary["alignment_genome_next"] = \
        seqsummary["alignment_genome"].shift(-1)
    seqsummary["alignment_genome_start_next"] = \
        seqsummary["alignment_genome_start"].shift(-1)
    seqsummary["alignment_genome_end_next"] = \
        seqsummary["alignment_genome_end"].shift(-1)
    seqsummary["bases_between_read_starts"] = (
        seqsummary["alignment_genome_start_next"]
        - seqsummary["alignment_genome_start"])
    seqsummary["bases_between_read_ends"] = (
        seqsummary["alignment_genome_end_next"]
        - seqsummary["alignment_genome_end"])
    seqsummary["bases_between_read_min"] = (
        seqsummary[["bases_between_read_starts", "bases_between_read_ends"]]
        .abs().min(axis=1))
    return seqsummary


def seqsummary_to_tempcompsummary(
        seqsummary: pd.DataFrame,
        max_time_between_reads: float = 20,
        max_seqlen_diff: float = 0.1,
        match_barcodes: bool = False,
        min_qscore: float = None,
        max_abs_seqlen_diff: int = None,
        ) -> pd.DataFrame:
    """Determine read pairs from annotated sequence summary."""
    logger = duplex_tools.get_named_logger("FindPairs")
    # Default filtering
    seqsummary["candidate_followon"] = (
        (-1.00 <= seqsummary["duration_until_next_start"])
        & (seqsummary["duration_until_next_start"] < max_time_between_reads))
    logger.info(f'{seqsummary["candidate_followon"].sum()} pairs after '
                f'filtering on duration between reads. (max '
                f'{max_time_between_reads} s)')

    seqsummary["candidate_followon"] = (
            seqsummary["candidate_followon"]
            & (seqsummary["fraction_missing_from_longest"] < max_seqlen_diff))
    logger.info(f'{seqsummary["candidate_followon"].sum()} pairs after '
                f'filtering on relative sequence length difference. (max '
                f'{max_seqlen_diff*100}% difference)')

    # Additional filtering
    if max_abs_seqlen_diff:
        seqsummary["candidate_followon"] = (
            seqsummary["candidate_followon"]
            & (seqsummary["sequence_length_difference"] < max_abs_seqlen_diff)
        )
        logger.info(f'{seqsummary["candidate_followon"].sum()} pairs after '
                    f'absolute sequence length filtering. ('
                    f'max {max_abs_seqlen_diff} bp)')

    try:
        if min_qscore:
            seqsummary["candidate_followon"] = (
                seqsummary["candidate_followon"]
                & (seqsummary["mean_qscore_template"] > min_qscore)
                & (seqsummary["mean_qscore_template_next"] > min_qscore)
            )
            logger.info(
                f'{seqsummary["candidate_followon"].sum()} pairs after '
                f'qscore filtering. (min qscore = {min_qscore})')

    except KeyError:
        logger.info("qscore data not available. Skipping the filter of "
                    f"min_qscore: {min_qscore}")

    if match_barcodes:
        first = seqsummary['barcode_arrangement']
        second = seqsummary["barcode_arrangement_next"]
        seqsummary["candidate_followon"] = (
            seqsummary["candidate_followon"] & (first == second))

    # first reads
    templates = seqsummary[seqsummary['candidate_followon']].copy()
    templates['pair_id'] = \
        templates['read_id'] + ' ' + templates['read_id_next']
    templates.dropna(inplace=True)
    # second reads
    complements = (
        seqsummary
        .set_index('read_id')
        .loc[templates['read_id_next']]
        .reset_index())
    complements['fraction_missing_from_longest'] = math.nan
    complements['duration_until_next_start'] = math.nan
    complements['sequence_length_difference'] = math.nan
    try:
        complements['mean_qscore_template_next'] = math.nan
    except KeyError:
        pass
    complements['pair_id'] = \
        complements['read_id_prev'] + ' ' + complements['read_id']
    # join first and seconds
    stats_per_read = pd.concat(
        [
            templates.assign(strand='template'),
            complements.assign(strand='complement')]
        ).sort_values(['pair_id', 'start_time'])

    return stats_per_read.drop(
        columns=[
            'candidate_followon', 'read_id_next', 'read_id_prev',
            'start_time_next', 'sequence_length_template_next'],
        errors='ignore')


def calculate_metrics_for_next_strand(
        seqsummary: pd.DataFrame) -> pd.DataFrame:
    """Calculate pairing metrics for read pairs.

    * fraction_missing_from_longest: The difference in sequence length between
      the pairs. Example: Would be 0.2 if one strand is 1000bp and the
      following one is 800bp (abs(1000bp-800bp)/1000bp)
    * duration_until_next_start: The duration between the end of one strand
      and the start of the next Example: Read 1 starts at 10s and is 5s long.
      Read 2 starts at 20s. Duration until next is 20-(10+15) = 5s
    """
    # ensure table is sorted and annotate next read info
    logger = duplex_tools.get_named_logger('FindPairs')
    seqsummary.sort_values(
        ["channel", "mux", "start_time"], inplace=True)
    # TODO: this isn't quite right, we need to group by channel and mux
    #       to analyse independently
    seqsummary["read_id_next"] = seqsummary["read_id"].shift(-1)
    seqsummary["read_id_prev"] = seqsummary["read_id"].shift(1)
    seqsummary["start_time_next"] = seqsummary["start_time"].shift(-1)
    seqsummary["sequence_length_template_next"] = \
        seqsummary["sequence_length_template"].shift(-1)

    seqsummary["sequence_length_difference"] = (seqsummary[
        "sequence_length_template_next"] - seqsummary[
        "sequence_length_template"]).abs()
    try:
        seqsummary["mean_qscore_template_next"] = \
            seqsummary["mean_qscore_template"].shift(-1)
    except KeyError:
        logger.debug('qscore not available in the summary. Cannot use for '
                     'metrics')
        pass

    seqsummary["end_time"] = seqsummary["start_time"] + seqsummary["duration"]

    # If there is barcode information (arrangement and scores),
    # then make it available for classification if necessary
    if "barcode_arrangement" in seqsummary.columns:
        seqsummary["barcode_arrangement_next"] = \
            seqsummary["barcode_arrangement"].shift(-1)
    if "barcode_front_score" in seqsummary.columns:
        seqsummary["barcode_front_score_next"] = \
            seqsummary["barcode_front_score"].shift(-1)
    if "barcode_rear_score" in seqsummary.columns:
        seqsummary["barcode_rear_score_next"] = \
            seqsummary["barcode_rear_score"].shift(-1)

    # difference between read lengths of pair
    bases_differing = (
        seqsummary["sequence_length_template_next"]
        - seqsummary["sequence_length_template"]).abs()
    # length of longest read in pair
    bases_longest = seqsummary[
        ["sequence_length_template_next", "sequence_length_template"]
        ].max(axis=1)
    # fractional length difference
    seqsummary["fraction_missing_from_longest"] = \
        bases_differing / bases_longest
    # duration in seconds between the end of the strand and the start of next
    seqsummary["duration_until_next_start"] = (
        seqsummary["start_time_next"] - seqsummary["end_time"])
    return seqsummary


def add_args(parser):
    """Add arguments specific to this process."""
    parser.add_argument(
        "--prefix", default="pair",
        help="")
    parser.add_argument(
        "--prepend_seqsummary_stem", action="store_true",
        help="Add filename of the sequencing summary to output files.")
    parser.add_argument(
        "--max_time_between_reads", type=int, default=200000,
        help=(
            "Maximum time (seconds) between reads for them to be "
            "deemed a pair."))
    parser.add_argument(
        "--max_seqlen_diff", type=float, default=0.1,
        help=(
            "Maximum ratio (a - b) / a, where a and b are the "
            "sequence lengths of a putative pair."))
    parser.add_argument(
        "--max_abs_seqlen_diff", type=int, default=5000,
        help=(
            "Maximum sequence length difference between template and "
            "complement"))
    parser.add_argument(
        "--min_qscore", type=float, default=6,
        help=(
            "The minimum simplex qscore required from both template and "
            "complement"))
    parser.add_argument(
        "--verbose", action="store_true",
        help="Logging level")
    parser.add_argument(
        "--match_barcodes", action="store_true",
        help="Require putative pair to contain same barcodes.")
    return parser


def argparser():
    """Create argument parser."""
    parser = ArgumentParser(
        "Create candidate pairs from sequencing summary.",
        formatter_class=ArgumentDefaultsHelpFormatter,
        parents=[duplex_tools._log_level()], add_help=False)
    parser.add_argument(
        "sequencing_summary",
        help="Sequencing summary file.")
    parser.add_argument(
        "output",
        help="Output directory.")
    parser = add_args(parser)

    return parser


def main(args):
    """Entry point."""
    find_pairs(
        sequencing_summary_path=args.sequencing_summary,
        outdir=args.output,
        prefix=args.prefix,
        prepend_seqsummary_stem=args.prepend_seqsummary_stem,
        max_time_between_reads=args.max_time_between_reads,
        max_seqlen_diff=args.max_seqlen_diff,
        match_barcodes=args.match_barcodes,
        min_qscore=args.min_qscore,
        max_abs_seqlen_diff=args.max_abs_seqlen_diff)
