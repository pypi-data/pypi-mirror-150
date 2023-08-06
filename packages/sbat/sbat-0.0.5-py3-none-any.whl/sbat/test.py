import bisect
import os
import datetime

import pandas as pd
from Bio import SeqIO
from pytz import utc

import analysis
import main
from dateutil.parser import parse as dparse

import utils

#
# def bin_nanopore(fastq, output, interval=1, subsamples=None):
#     file_type = 'fastq' if fastq.split('.')[-1] == 'fastq' else 'fasta'
#
#     batchfiles = []
#     start = utc.localize(datetime.datetime.now())
#     end = utc.localize(datetime.datetime(1970, 1, 1, 0, 0, 0))
#
#     for record in SeqIO.parse(fastq, file_type):
#         record_time = dparse([i for i in record.description.split() if i.startswith('start_time')][0].split('=')[1])
#         if record_time < start:
#             start = record_time
#         if record_time > end:
#             end = record_time
#     batches = analysis.hours_aligned(start, end, interval)
#     sequences_per_batch = [0 for _ in range(len(batches))]
#     bases_per_batch = [0 for _ in range(len(batches))]
#
#     for record in SeqIO.parse(fastq, file_type):
#
#         record_time = dparse([i for i in record.description.split() if i.startswith('start_time')][0].split('=')[1])
#         batch = bisect.bisect_left(batches, record_time)
#         if subsamples is not None and bases_per_batch[batch] >= subsamples: #sequences_per_batch[batch] >= subsamples:
#             continue
#         sequences_per_batch[batch] += 1
#         bases_per_batch[batch] += len(record.seq)
#         filename = utils.unique_path(os.path.join(output, analysis.NANOPORE_BIN_FORMAT.format(utils.get_filename(fastq), batch)))
#         if filename not in batchfiles:
#             batchfiles.append(filename)
#         f = open(filename, 'a')
#         f.write(record.format('fasta'))
#         f.close()
#
#     analysis.plot_bin_distribution(sequences_per_batch, utils.get_filename(fastq) + "_subsamples")
#     return batchfiles
#
# #print(bin_nanopore("nanopore/per_2h/nanopore_GM24385_11.fasta", subsamples=50000000))
# # all = []
# # for i in range(49):
# #      count = 0
# #      for record in SeqIO.parse(r"nanopore\subsamples\nanopore_nanopore_GM24385_11_batch_"  + str(i) +".fasta", "fasta"):
# #           count += len(record.seq)
# #      print("batch {0}: {1}".format(i, count))
# #      all.append(count)
# #
# # analysis.plot_bin_distribution(all, "nanopore_subsampling_20k_reads")
# a = analysis.Analysis(output_dir="out")
# df = pd.read_csv("out/sbat/dump/df_output_5_nanopore_GM24385_11.csv")
# a.plot_kmers_vs_bias(df)


#
#
#
#
# def track_most_common_kmer_change_freq(dfs, k):
#     fwds, bwds = utils.split_forwards_and_backwards(k)
#     fwds = fwds.sort()
#     kmer_changes = pd.DataFrame(
#         data={'seq': fwds},
#         columns=['seq'])
#     for batch, df in enumerate(dfs):
#         df["more_freq_count"] = df.apply(lambda row: utils.select_more_frequent(row), axis=1)
#         df = df.sort_values(by=['seq'])[['seq', 'strand_bias_%', 'more_freq_count', 'GC_%']]
#         kmer_changes = kmer_changes.merge(df, how='right', on='seq', suffixes=("", "_batch_{}".format(batch))).dropna()
#
#     kmer_changes.rename({'strand_bias_%': 'strand_bias_%_batch_0'}, inplace=True)
#     kmer_changes = kmer_changes.sort_values(by=['more_freq_count'], ascending=False)
#     kmer_changes['diff'] = abs(kmer_changes['strand_bias_%_batch_20'] - kmer_changes['strand_bias_%'])
#
#
#     plt.figure(figsize=(35, 10))
#     plt.title("K-mers of length ordered by frequency {} vs strand bias delta".format(k), fontsize=18)
#     plt.xlabel('K-mers', fontsize=18)
#     plt.ylabel('Strand bias delta [%]', fontsize=18)
#     ax = plt.scatter(kmer_changes['strand_bias_%'], kmer_changes['diff'], marker="o", color="blue", s=6)
#     plt.show()
#
#     return kmer_changes
#
# dfs = []
# for i in range(0, 48):
#     df = pd.read_csv(r'D:\Alex\School\sbapr\strand-bias-analysis-tool\sbat\nano_full\sbat_out\dump\df_output_6_nanopore_nanopore_GM24385_11_batch_{}.csv'.format(i))
#     dfs.append(df)
#
#
# a = analysis.Analysis(output_dir="nano_full")
# a.set_file("GM24385_1.fasta")
# a.track_most_common_kmer_change_freq(dfs, 5)
# a.track_most_common_kmer_change_freq(dfs, 6)
#df7 = pd.read_csv('D:\Alex\School\sbapr\strand-bias-analysis-tool\out\sbat\dump\df_output_5_nanopore_41ec7eae4495de82ef09c416dbd6d5c983ff8c4e_batch_2.csv')
#
#
# r = track_most_common_kmer_change_freq(dfs, 7)
# fastq = "../out/a9a16b6dde58dfd690ae7daa3bcf9145cad21ac0.fasta"
# filename = utils.get_filename(fastq) + "subs_200m.fastq"
# bases_limit = 200000000
# bases_count = 0
# reads_count = 0
# reads_limit = 100000
# subsampling = False
#
# for record in SeqIO.parse(fastq, 'fasta'):
#     if subsampling and (
#             bases_count >= bases_limit):
#         break
#     reads_count += 1
#     bases_count += len(record.seq)
#     # if subsampling:
#     #     f = open(filename, 'a')
#     #     f.write(record.format('fasta'))
#     #     f.close()
#
# print(bases_count)
# print(reads_count)

import cProfile, pstats

profiler = cProfile.Profile()
profiler.enable()
utils.split_forwards_and_backwards(15)
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()