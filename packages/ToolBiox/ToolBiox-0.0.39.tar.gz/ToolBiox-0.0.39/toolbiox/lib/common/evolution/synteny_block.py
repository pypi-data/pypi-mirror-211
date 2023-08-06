import pandas as pd
from toolbiox.lib.common.genome.genome_feature2 import read_gff_file, GenomeFeature
from toolbiox.lib.common.genome.seq_base import read_fasta_by_faidx
from collections import OrderedDict
from toolbiox.lib.common.os import multiprocess_running
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as Patches
import re
from toolbiox.lib.common.math.set import merge_same_element_set
from toolbiox.lib.common.math.interval import merge_intervals
from interlap import InterLap


class GeneLoci(GenomeFeature):
    def __init__(self, gene_id, chr_id, loci, species=None, gf=None):
        if gf:
            gf.sp_id = species
            gf.chr_id = chr_id
            gf.id = gene_id
            super(GeneLoci, self).__init__(id=gene_id, chr_loci=gf, sp_id=gf.sp_id,
                                           type=gf.type, qualifiers=gf.qualifiers, sub_features=gf.sub_features)
        else:
            super(GeneLoci, self).__init__(id=gene_id, type=None, chr_loci=None, qualifiers={},
                                           sub_features=None, chr_id=chr_id, strand=None, start=None, end=None, sp_id=species)
        self.loci = loci
        self.gf = gf

    def __str__(self):
        return "%s: No. %d gene on %s from %s" % (self.id, self.loci, self.chr_id, self.sp_id)


class Genome(object):
    def __init__(self, species_prefix, gff3_file=None, fasta_file=None):
        self.chr_dict = {}
        self.gene_dict = {}
        self.chr_length_dict = {}
        self.id = species_prefix

        if gff3_file:
            gff_dict = read_gff_file(gff3_file)

            chr_dict = {}
            gene_dict = {}
            for i in gff_dict['gene']:
                gf = gff_dict['gene'][i]
                if not gf.chr_id in chr_dict:
                    chr_dict[gf.chr_id] = []
                chr_dict[gf.chr_id].append(gf)
                gene_dict[gf.id] = gf

            for chr_id in chr_dict:
                chr_dict[chr_id] = sorted(
                    chr_dict[chr_id], key=lambda x: x.start)

            chr_gene_id_dict = {}
            for chr_id in chr_dict:
                chr_gene_id_dict[chr_id] = [i.id for i in chr_dict[chr_id]]

            self.chr_dict = {}
            self.gene_dict = {}
            for chr_id in chr_gene_id_dict:
                num = 0
                self.chr_dict[chr_id] = OrderedDict()
                for gene_id in chr_gene_id_dict[chr_id]:
                    gene = GeneLoci(gene_id, chr_id, num,
                                    species_prefix, gene_dict[gene_id])
                    self.chr_dict[chr_id][num] = gene
                    self.gene_dict[gene_id] = gene
                    num += 1

            self.chr_length_dict = {}
            if fasta_file:
                fa_dict = read_fasta_by_faidx(fasta_file)
                self.chr_length_dict = {i: fa_dict[i].len() for i in fa_dict}
            else:
                for chr_id in self.chr_dict:
                    self.chr_length_dict[chr_id] = max(
                        [self.chr_dict[chr_id][i].end for i in self.chr_dict[chr_id]])

            self.chr_gene_number_dict = {}
            for chr_id in self.chr_dict:
                self.chr_gene_number_dict[chr_id] = len(
                    self.chr_dict[chr_id])


class GenePair(object):
    def __init__(self, q_gene, s_gene, property_dict=None):
        self.q_gene = q_gene
        self.s_gene = s_gene
        self.property = property_dict

    def __str__(self):
        return "%s vs %s" % (self.q_gene.id, self.s_gene.id)

    def reverse_myself(self):
        new_GP = GenePair(self.s_gene, self.q_gene, self.property)
        return new_GP


class SyntenyBlock(object):
    def __init__(self, sb_id, q_sp, s_sp, strand, gene_pair_dict, property_dict, parameter_dict):
        self.id = sb_id
        self.property = property_dict
        self.parameter = parameter_dict
        self.strand = strand
        self.q_sp = q_sp
        self.s_sp = s_sp
        self.gene_pair_dict = gene_pair_dict

        if len(gene_pair_dict) > 0:
            self.get_info()

    def get_info(self):
        self.q_chr = self.gene_pair_dict[0].q_gene.chr_id
        self.s_chr = self.gene_pair_dict[0].s_gene.chr_id

        q_gene_list = sorted(
            [self.gene_pair_dict[i].q_gene for i in self.gene_pair_dict], key=lambda x: x.loci)
        self.first_q_gene = q_gene_list[0]
        self.last_q_gene = q_gene_list[-1]

        s_gene_list = sorted(
            [self.gene_pair_dict[i].s_gene for i in self.gene_pair_dict], key=lambda x: x.loci)
        self.first_s_gene = s_gene_list[0]
        self.last_s_gene = s_gene_list[-1]

        self.first_q_gene_loci = self.first_q_gene.loci
        self.last_q_gene_loci = self.last_q_gene.loci
        self.first_s_gene_loci = self.first_s_gene.loci
        self.last_s_gene_loci = self.last_s_gene.loci

        self.query_from = min([self.first_q_gene.gf.start, self.first_q_gene.gf.end,
                               self.last_q_gene.gf.start, self.last_q_gene.gf.end])
        self.query_to = max([self.first_q_gene.gf.start, self.first_q_gene.gf.end,
                             self.last_q_gene.gf.start, self.last_q_gene.gf.end])

        self.subject_from = min([self.first_s_gene.gf.start, self.first_s_gene.gf.end,
                                 self.last_s_gene.gf.start, self.last_s_gene.gf.end])
        self.subject_to = max([self.first_s_gene.gf.start, self.first_s_gene.gf.end,
                               self.last_s_gene.gf.start, self.last_s_gene.gf.end])

    def get_full_info(self, q_genome, s_genome):
        self.get_info()

        self.query_gene_list = []
        for i in range(self.first_q_gene_loci, self.last_q_gene_loci + 1):
            self.query_gene_list.append(q_genome.chr_dict[self.q_chr][i])

        self.subject_gene_list = []
        for i in range(self.first_s_gene_loci, self.last_s_gene_loci + 1):
            self.subject_gene_list.append(s_genome.chr_dict[self.s_chr][i])

    def reverse_myself(self, new_sb_id=None):
        gene_pair_dict = {
            i: self.gene_pair_dict[i].reverse_myself() for i in self.gene_pair_dict}
        if new_sb_id is None:
            new_sb_id = self.id

        new_sb = SyntenyBlock(new_sb_id, self.s_sp, self.q_sp,
                              self.strand, gene_pair_dict, self.property, self.parameter)

        new_sb.q_chr = new_sb.gene_pair_dict[0].q_gene.chr_id
        new_sb.s_chr = new_sb.gene_pair_dict[0].s_gene.chr_id

        new_sb.query_gene_list = self.subject_gene_list
        new_sb.subject_gene_list = self.query_gene_list

        new_sb.first_q_gene = self.first_s_gene
        new_sb.last_q_gene = self.last_s_gene
        new_sb.first_s_gene = self.first_q_gene
        new_sb.last_s_gene = self.last_q_gene

        new_sb.first_q_gene_loci = new_sb.first_q_gene.loci
        new_sb.last_q_gene_loci = new_sb.last_q_gene.loci
        new_sb.first_s_gene_loci = new_sb.first_s_gene.loci
        new_sb.last_s_gene_loci = new_sb.last_s_gene.loci

        new_sb.query_from = self.subject_from
        new_sb.query_to = self.subject_to
        new_sb.subject_from = self.query_from
        new_sb.subject_to = self.query_to

        return new_sb

    def __str__(self):

        return "Q = %s:%s gene: %d-%d (%d) base: %d-%d (%d) vs S = %s:%s gene: %d-%d (%d) base: %d-%d (%d), %s, have %d gene pair" % (self.q_sp, self.q_chr, self.first_q_gene_loci, self.last_q_gene_loci, self.last_q_gene_loci - self.first_q_gene_loci + 1,  self.query_from, self.query_to, self.query_to - self.query_from + 1, self.s_sp, self.s_chr, self.first_s_gene_loci, self.last_s_gene_loci, self.last_s_gene_loci - self.first_s_gene_loci + 1,   self.subject_from, self.subject_to, self.subject_to - self.subject_from + 1, self.strand, len(self.gene_pair_dict))

    __repr__ = __str__


def merge_blocks(synteny_block_dict, q_genome, s_genome):
    merged_group_list = get_overlaped_block_group(synteny_block_dict)
    num = 0
    merged_synteny_block_dict = {}
    for group_list in merged_group_list:
        merged_synteny_block_dict[num] = get_merged_block(
            num, group_list, synteny_block_dict, q_genome, s_genome)
        num += 1
    return merged_synteny_block_dict


def get_merged_block(merge_id, group_list, synteny_block_dict, q_genome, s_genome):
    tmp_sb = synteny_block_dict[sorted(group_list, key=lambda x:(abs(
        synteny_block_dict[x].query_to - synteny_block_dict[x].query_from)), reverse=True)[0]]
    q_sp = tmp_sb.q_sp
    s_sp = tmp_sb.s_sp
    strand = tmp_sb.strand
    parameter_dict = tmp_sb.parameter

    gene_pair_dict = {}
    num = 0
    for i in group_list:
        for j in synteny_block_dict[i].gene_pair_dict:
            gene_pair_dict[num] = synteny_block_dict[i].gene_pair_dict[j]
            num += 1

    super_sb = SyntenyBlock(merge_id, q_sp, s_sp, strand,
                            gene_pair_dict, {}, parameter_dict)

    super_sb.get_full_info(q_genome, s_genome)

    return super_sb


def get_overlaped_block_group(synteny_block_dict):
    q_sb_interlap, s_sb_interlap = get_synteny_block_interlap(
        synteny_block_dict)

    group_list = []
    for sb_id in synteny_block_dict:
        group_list.append([sb_id])
        sb = synteny_block_dict[sb_id]

        q_over_list = [i[2] for i in q_sb_interlap[sb.q_chr].find(
            (sb.first_q_gene_loci, sb.last_q_gene_loci))]
        s_over_list = [i[2] for i in s_sb_interlap[sb.s_chr].find(
            (sb.first_s_gene_loci, sb.last_s_gene_loci))]

        overlap_list = list(set(q_over_list) & set(s_over_list))

        if len(overlap_list) > 0:
            # print(overlap_list)
            group_list.append(overlap_list)

    merged_group_list = merge_same_element_set(group_list)

    return merged_group_list


def get_synteny_block_interlap(synteny_block_dict):
    query_synteny_block_chr_interlap_dict = {}
    subject_synteny_block_chr_interlap_dict = {}
    for sb_id in synteny_block_dict:
        sb = synteny_block_dict[sb_id]
        q_chr = sb.q_chr
        s_chr = sb.s_chr
        query_synteny_block_chr_interlap_dict[q_chr] = InterLap()
        subject_synteny_block_chr_interlap_dict[s_chr] = InterLap()

    for sb_id in synteny_block_dict:
        sb = synteny_block_dict[sb_id]
        q_chr = sb.q_chr
        s_chr = sb.s_chr

        query_synteny_block_chr_interlap_dict[q_chr].add(
            (sb.first_q_gene_loci, sb.last_q_gene_loci, sb_id))
        subject_synteny_block_chr_interlap_dict[s_chr].add(
            (sb.first_s_gene_loci, sb.last_s_gene_loci, sb_id))

    return query_synteny_block_chr_interlap_dict, subject_synteny_block_chr_interlap_dict


def gene_cover_depth_stat(synteny_block_dict, query_or_subject, covered_genome):
    q_sb_interlap, s_sb_interlap = get_synteny_block_interlap(
        synteny_block_dict)

    if query_or_subject == 'query':
        sb_interlap = q_sb_interlap
    elif query_or_subject == 'subject':
        sb_interlap = s_sb_interlap

    # gene cover dict
    gene_cover_depth_dict = {}
    for g_id in covered_genome.gene_dict:
        gene = covered_genome.gene_dict[g_id]
        if gene.chr_id in sb_interlap:
            gene_cover_depth_dict[g_id] = len(
                list(sb_interlap[gene.chr_id].find((gene.loci, gene.loci))))
        else:
            gene_cover_depth_dict[g_id] = 0

    # range cover
    range_loci_cover_chr_dict = {}
    for chr_id in covered_genome.chr_dict:
        range_loci_cover_chr_dict[chr_id] = {}
        for gene_num in covered_genome.chr_dict[chr_id]:
            g = covered_genome.chr_dict[chr_id][gene_num]
            g_depth = gene_cover_depth_dict[g.id]
            if g_depth == 0:
                continue
            if g_depth not in range_loci_cover_chr_dict[chr_id]:
                range_loci_cover_chr_dict[chr_id][g_depth] = []
            range_loci_cover_chr_dict[chr_id][g_depth].append(
                (gene_num, gene_num))
            range_loci_cover_chr_dict[chr_id][g_depth] = merge_intervals(
                range_loci_cover_chr_dict[chr_id][g_depth], True)

    range_base_cover_chr_dict = {}
    for chr_id in range_loci_cover_chr_dict:
        range_base_cover_chr_dict[chr_id] = {}
        for depth in range_loci_cover_chr_dict[chr_id]:
            if depth == 0:
                continue
            range_base_cover_chr_dict[chr_id][depth] = []

            for s, e in range_loci_cover_chr_dict[chr_id][depth]:
                start = covered_genome.chr_dict[chr_id][s].gf.start
                end = covered_genome.chr_dict[chr_id][e].gf.end
                range_base_cover_chr_dict[chr_id][depth].append((start, end))

    return gene_cover_depth_dict, range_loci_cover_chr_dict, range_base_cover_chr_dict


class wgdi_collinearity:
    def __init__(self, options, points):
        self.gap_penality = -1
        self.over_length = 0
        self.mg1 = 40
        self.mg2 = 40
        self.pvalue = 1
        self.over_gap = 5
        self.points = points
        self.p_value = 0
        self.coverage_ratio = 0.8
        for k, v in options:
            setattr(self, str(k), v)
        if hasattr(self, 'grading'):
            self.grading = [int(k) for k in self.grading.split(',')]
        else:
            self.grading = [50, 40, 25]
        # if hasattr(self, 'mg'):
        #     self.mg1, self.mg2 = [int(k) for k in self.mg.split(',')]
        # else:
        #     self.mg1, self.mg2 = [40, 40]
        self.pvalue = float(self.pvalue)
        self.coverage_ratio = float(self.coverage_ratio)

    def get_martix(self):
        self.points['usedtimes1'] = 0
        self.points['usedtimes2'] = 0
        self.points['times'] = 1
        self.points['score1'] = self.points['grading']
        self.points['score2'] = self.points['grading']
        self.points['path1'] = self.points.index.to_numpy().reshape(
            len(self.points), 1).tolist()
        self.points['path2'] = self.points['path1']
        self.points_init = self.points.copy()
        self.mat_points = self.points

    def run(self):
        self.get_martix()
        self.score_matrix()
        data = []
        # plus
        points1 = self.points[['loc1', 'loc2',
                               'score1', 'path1', 'usedtimes1']]
        points1 = points1.sort_values(by=['score1'], ascending=[False])
        points1.drop(
            index=points1[points1['usedtimes1'] < 1].index, inplace=True)
        points1.columns = ['loc1', 'loc2', 'score', 'path', 'usedtimes']
        while (self.over_length >= self.over_gap or len(points1) >= self.over_gap):
            if self.maxPath(points1):
                if self.p_value > self.pvalue:
                    continue
                data.append([self.path, self.p_value, self.score])
        # minus
        points2 = self.points[['loc1', 'loc2',
                               'score2', 'path2', 'usedtimes2']]
        points2 = points2.sort_values(by=['score2'], ascending=[False])
        points2.drop(
            index=points2[points2['usedtimes2'] < 1].index, inplace=True)
        points2.columns = ['loc1', 'loc2', 'score', 'path', 'usedtimes']
        while (self.over_length >= self.over_gap) or (len(points2) >= self.over_gap):
            if self.maxPath(points2):
                if self.p_value > self.pvalue:
                    continue
                data.append([self.path, self.p_value, self.score])
        return data

    def score_matrix(self):
        for index, row, col in self.points[['loc1', 'loc2', ]].itertuples():
            points = self.points[(self.points['loc1'] > row) & (self.points['loc2'] > col) & (
                self.points['loc1'] < row+self.mg1) & (self.points['loc2'] < col+self.mg2)]
            row_i_old, gap = row, self.mg2
            for index_ij, row_i, col_j, grading in points[['loc1', 'loc2', 'grading']].itertuples():
                if col_j - col > gap and row_i > row_i_old:
                    break
                s = grading + (row_i-row+col_j-col)*self.gap_penality
                s1 = s+self.points.at[index, 'score1']
                if s > 0 and self.points.at[index_ij, 'score1'] < s1:
                    self.points.at[index_ij, 'score1'] = s1
                    self.points.at[index, 'usedtimes1'] += 1
                    self.points.at[index_ij, 'usedtimes1'] += 1
                    self.points.at[index_ij,
                                   'path1'] = self.points.at[index, 'path1']+[index_ij]
                    gap = min(col_j-col, gap)
                    row_i_old = row_i
        points_revese = self.points.sort_values(
            by=['loc1', 'loc2'], ascending=[False, True])
        for index, row, col in points_revese[['loc1', 'loc2']].itertuples():
            points = points_revese[(points_revese['loc1'] < row) & (points_revese['loc2'] > col) & (
                points_revese['loc1'] > row-self.mg1) & (points_revese['loc2'] < col+self.mg2)]
            row_i_old, gap = row, self.mg2
            for index_ij, row_i, col_j, grading in points[['loc1', 'loc2', 'grading']].itertuples():
                if col_j - col > gap and row_i < row_i_old:
                    break
                s = grading + (row-row_i+col_j-col)*self.gap_penality
                s1 = s + self.points.at[index, 'score2']
                if s > 0 and self.points.at[index_ij, 'score2'] < s1:
                    self.points.at[index_ij, 'score2'] = s1
                    self.points.at[index, 'usedtimes2'] += 1
                    self.points.at[index_ij, 'usedtimes2'] += 1
                    self.points.at[index_ij,
                                   'path2'] = self.points.at[index, 'path2']+[index_ij]
                    gap = min(col_j-col, gap)
                    row_i_old = row_i
        return self.points

    def maxPath(self, points):
        if len(points) == 0:
            self.over_length = 0
            return False
        self.score, self.path_index = points.loc[points.index[0], [
            'score', 'path']]
        self.path = points[points.index.isin(self.path_index)]
        self.over_length = len(self.path_index)
        # Whether the block overlaps with other blocks
        if self.over_length >= self.over_gap and len(self.path)/self.over_length > self.coverage_ratio:
            points.drop(index=self.path.index, inplace=True)
            [[loc1_min, loc2_min], [loc1_max, loc2_max]] = self.path[[
                'loc1', 'loc2']].agg(['min', 'max']).to_numpy()
            # calculate pvalues
            gap_init = self.points_init[(loc1_min <= self.points_init['loc1']) & (self.points_init['loc1'] <= loc1_max) &
                                        (loc2_min <= self.points_init['loc2']) & (self.points_init['loc2'] <= loc2_max)].copy()
            self.p_value = self.pvalue_estimated(
                gap_init, loc1_max-loc1_min+1, loc2_max-loc2_min+1)
            self.path = self.path.sort_values(by=['loc1'], ascending=[True])[
                ['loc1', 'loc2']]
            return True
        else:
            points.drop(index=points.index[0], inplace=True)
        return False

    def pvalue_estimated(self, gap, L1, L2):
        N1 = gap['times'].sum()
        N = len(gap)
        self.points_init.loc[gap.index, 'times'] += 1
        m = len(self.path)
        a = (1-self.score/m/self.grading[0])*(N1-m+1)/N*(L1-m+1)*(L2-m+1)/L1/L2
        return round(a, 4)

# wgdi functions


def run_wgdi_collinearity(loc_pair_list, min_size=5, max_gap=25, max_pvalue=1, min_score=50, gap_penality=-1, **kargs):
    """
    loc_pair_list = [
        (8, 1618), # loc of homo gene pair
        (11, 273),
    ]

    return data.append([self.path, self.p_value, self.score])
    """

    loc_pair_list = sorted(loc_pair_list, key=lambda x: x[0])

    options = {
        "gap_penality": gap_penality,
        "over_length": 0,
        # The maximum gap(mg) value is an important parameter for detecting collinear regions.
        "mg1": max_gap,
        # The maximum gap(mg) value is an important parameter for detecting collinear regions.
        "mg2": max_gap,
        # Evaluate the compactness and uniqueness of collinear blocks, the range is 0-1, and the better collinearity range is 0-0.2.
        "pvalue": 1,
        "over_gap": 5,
        "p_value": 0,
        "coverage_ratio": 0.8,
    }

    for i in kargs:
        options[i] = kargs[i]

    loc1 = [i[0] for i in loc_pair_list]
    loc2 = [i[1] for i in loc_pair_list]

    df = pd.DataFrame(
        {
            'loc1': loc1,
            'loc2': loc2,
            'grading': 50,
        }
    )

    options = [(i, options[i]) for i in options]
    my_collinearity = wgdi_collinearity(
        options, df)

    data = my_collinearity.run()
    data = [i for i in data if len(
        i[0]) >= min_size and i[1] <= max_pvalue and i[2] >= min_score]

    return data


def get_synteny_block(gene_pair_list, min_size=5, max_gap=25, max_pvalue=1, min_score=50, gap_penality=-1, tandem_repeat_gap=10):
    for gp in gene_pair_list:
        q = gp.q_gene
        s = gp.s_gene

        if q.sp_id == s.sp_id and q.chr_id == s.chr_id and abs(q.loci-s.loci) <= tandem_repeat_gap:
            gp.is_tandem = True
        else:
            gp.is_tandem = False

    loc_pair_list = [(gp.q_gene.loci, gp.s_gene.loci)
                     for gp in gene_pair_list if not gp.is_tandem]

    q_sp = gene_pair_list[0].q_gene.sp_id
    s_sp = gene_pair_list[0].s_gene.sp_id

    q_gene_dict = {gp.q_gene.loci: gp.q_gene for gp in gene_pair_list}
    s_gene_dict = {gp.s_gene.loci: gp.s_gene for gp in gene_pair_list}

    parameter_dict = {
        "min_size": min_size,
        "max_gap": max_gap,
        "max_pvalue": max_pvalue,
        "min_score": min_score,
        "gap_penality": gap_penality
    }

    wgdi_out_list = run_wgdi_collinearity(
        loc_pair_list, min_size, max_gap, max_pvalue, min_score, gap_penality)

    num = 0
    output_dict = OrderedDict()
    for wgdi_out in wgdi_out_list:
        sb_df, p_value, score = wgdi_out

        property_dict = {
            'score': score,
            'p_value': p_value,
            'gene_pair_num': len(sb_df),
        }

        a, b = sb_df['loc2'].head(2).values
        if a < b:
            strand = '+'
        else:
            strand = '-'

        gene_pair_dict = OrderedDict([(i, GenePair(
            q_gene_dict[sb_df.iloc[i].loc1], s_gene_dict[sb_df.iloc[i].loc2])) for i in range(len(sb_df))])

        sb = SyntenyBlock(num, q_sp, s_sp, strand,
                          gene_pair_dict, property_dict, parameter_dict)

        output_dict[num] = sb
        num += 1

    return output_dict


class DotPlotJob(object):
    def __init__(self, sp1, sp2, synteny_block_dict, sp1_base_cover_dict=None, sp2_base_cover_dict=None, sp1_loci_cover_dict=None, sp2_loci_cover_dict=None):
        self.sp1 = sp1
        self.sp2 = sp2
        self.synteny_block_dict = synteny_block_dict
        self.sp1_base_cover_dict = sp1_base_cover_dict
        self.sp2_base_cover_dict = sp2_base_cover_dict
        self.sp1_loci_cover_dict = sp1_loci_cover_dict
        self.sp2_loci_cover_dict = sp2_loci_cover_dict

    def plot(self, mode='base', sp1_top=None, sp2_top=None, reverse=False, max_cover_depth=4, save_file=None, sp1_contig_list=None, sp2_contig_list=None, min_contig_length=1000000, min_loci_number=50):
        # parameter
        fig_size = (20, 20)

        # make fig & ax
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0.02
        cover_plot_height = 0.04

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom - cover_plot_height -
                      spacing, width, cover_plot_height]
        rect_histy = [left + width + spacing*1.5,
                      bottom, cover_plot_height, height]

        fig = plt.figure(figsize=fig_size)

        ax = fig.add_axes(rect_scatter)
        ax_histx = fig.add_axes(rect_histx, sharex=ax)
        ax_histy = fig.add_axes(rect_histy, sharey=ax)

        if mode == 'base':
            if not sp1_contig_list:
                sp1_contig_list = [i[0] for i in sorted(self.sp1.chr_length_dict.items(
                ), key=lambda x: x[1], reverse=True) if i[1] > min_contig_length]

            if not sp2_contig_list:
                sp2_contig_list = [i[0] for i in sorted(self.sp2.chr_length_dict.items(
                ), key=lambda x: x[1], reverse=True) if i[1] > min_contig_length]
        elif mode == 'loci':
            if not sp1_contig_list:
                sp1_contig_list = [i[0] for i in sorted(self.sp1.chr_gene_number_dict.items(
                ), key=lambda x: x[1], reverse=True) if i[1] > min_loci_number]

            if not sp2_contig_list:
                sp2_contig_list = [i[0] for i in sorted(self.sp2.chr_gene_number_dict.items(
                ), key=lambda x: x[1], reverse=True) if i[1] > min_loci_number]

        if mode == 'base':
            if reverse:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, self.sp2.chr_length_dict, self.sp1.chr_length_dict, sp2_top, sp1_top, q_contig_list=sp2_contig_list, s_contig_list=sp1_contig_list)
                self.add_synteny_dot(ax, query_contig_coord, subject_contig_coord,
                                     self.synteny_block_dict, reverse=reverse)

                self.small_cover_plot(ax_histx, 'h', self.sp1_base_cover_dict,
                                      subject_contig_coord, max_cover_depth=max_cover_depth)
                self.small_cover_plot(ax_histy, 'v', self.sp2_base_cover_dict,
                                      query_contig_coord, max_cover_depth=max_cover_depth)

                ax.set_xlabel(self.sp1.id, fontsize=20)
                ax.set_ylabel(self.sp2.id, fontsize=20)
            else:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, self.sp1.chr_length_dict, self.sp2.chr_length_dict, sp1_top, sp2_top, q_contig_list=sp1_contig_list, s_contig_list=sp2_contig_list)
                self.add_synteny_dot(ax, query_contig_coord, subject_contig_coord,
                                     self.synteny_block_dict, reverse=reverse)

                self.small_cover_plot(ax_histx, 'h', self.sp2_base_cover_dict,
                                      subject_contig_coord, max_cover_depth=max_cover_depth)
                self.small_cover_plot(ax_histy, 'v', self.sp1_base_cover_dict,
                                      query_contig_coord, max_cover_depth=max_cover_depth)

                ax.set_xlabel(self.sp2.id, fontsize=20)
                ax.set_ylabel(self.sp1.id, fontsize=20)
        elif mode == 'loci':
            if reverse:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, self.sp2.chr_gene_number_dict, self.sp1.chr_gene_number_dict, sp2_top, sp1_top, q_contig_list=sp2_contig_list, s_contig_list=sp1_contig_list)
                self.add_synteny_dot(ax, query_contig_coord, subject_contig_coord,
                                     self.synteny_block_dict, mode=mode, reverse=reverse)

                self.small_cover_plot(ax_histx, 'h', self.sp1_loci_cover_dict,
                                      subject_contig_coord, max_cover_depth=max_cover_depth)
                self.small_cover_plot(ax_histy, 'v', self.sp2_loci_cover_dict,
                                      query_contig_coord, max_cover_depth=max_cover_depth)

                ax.set_xlabel(self.sp1.id, fontsize=20)
                ax.set_ylabel(self.sp2.id, fontsize=20)
            else:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, self.sp1.chr_gene_number_dict, self.sp2.chr_gene_number_dict, sp1_top, sp2_top, q_contig_list=sp1_contig_list, s_contig_list=sp2_contig_list)
                self.add_synteny_dot(ax, query_contig_coord, subject_contig_coord,
                                     self.synteny_block_dict, mode=mode, reverse=reverse)

                self.small_cover_plot(ax_histx, 'h', self.sp2_loci_cover_dict,
                                      subject_contig_coord, max_cover_depth=max_cover_depth)
                self.small_cover_plot(ax_histy, 'v', self.sp1_loci_cover_dict,
                                      query_contig_coord, max_cover_depth=max_cover_depth)

                ax.set_xlabel(self.sp2.id, fontsize=20)
                ax.set_ylabel(self.sp1.id, fontsize=20)

        ax.xaxis.set_label_position('bottom')
        ax.xaxis.set_label_coords(0.5, -0.01)
        ax.yaxis.set_label_position('right')
        ax.yaxis.set_label_coords(1.01, 0.5)

        plt.show()

        if save_file:
            fig.savefig(save_file, format='pdf', facecolor='none',
                        edgecolor='none', bbox_inches='tight')

    def small_cover_plot(self, ax, orientation, base_cover_chr_dict, contig_coord, max_cover_depth=5, facecolor='r'):

        rectangle_list = []
        for chr_id in base_cover_chr_dict:
            for depth in base_cover_chr_dict[chr_id]:
                for s, e in base_cover_chr_dict[chr_id][depth]:
                    if chr_id not in contig_coord:
                        continue
                    contig_coord_base = contig_coord[chr_id]
                    ps, pe = s+contig_coord_base, e+contig_coord_base
                    if orientation == 'h':
                        rect = Patches.Rectangle((ps, 0), pe-ps, depth)
                    elif orientation == 'v':
                        rect = Patches.Rectangle((0, ps), depth, pe-ps)
                    rectangle_list.append(rect)

        pc = PatchCollection(
            rectangle_list, facecolor=facecolor, edgecolor='None')
        ax.add_collection(pc)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if orientation == 'h':
            ax.set_ylim((0, max_cover_depth+0.5))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1))
            ax.get_xaxis().set_visible(False)

        elif orientation == 'v':
            ax.set_xlim((0, max_cover_depth+0.5))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
            ax.get_yaxis().set_visible(False)

    def add_synteny_dot(self, ax, query_contig_coord, subject_contig_coord, synteny_block_dict, mode='base', reverse=False, color='#617a95', linewidth=3):
        for id_tmp in synteny_block_dict:
            sb_tmp = synteny_block_dict[id_tmp]
            strand = sb_tmp.strand

            if not reverse:
                q_id = sb_tmp.q_chr
                s_id = sb_tmp.s_chr
                if mode == 'base':
                    q_f = sb_tmp.query_from
                    q_t = sb_tmp.query_to
                    s_f = sb_tmp.subject_from
                    s_t = sb_tmp.subject_to
                elif mode == 'loci':
                    q_f = sb_tmp.first_q_gene_loci
                    q_t = sb_tmp.last_q_gene_loci
                    s_f = sb_tmp.first_s_gene_loci
                    s_t = sb_tmp.last_s_gene_loci
            else:
                q_id = sb_tmp.s_chr
                s_id = sb_tmp.q_chr
                if mode == 'base':
                    q_f = sb_tmp.subject_from
                    q_t = sb_tmp.subject_to
                    s_f = sb_tmp.query_from
                    s_t = sb_tmp.query_to
                elif mode == 'loci':
                    q_f = sb_tmp.first_s_gene_loci
                    q_t = sb_tmp.last_s_gene_loci
                    s_f = sb_tmp.first_q_gene_loci
                    s_t = sb_tmp.last_q_gene_loci

            if q_id not in query_contig_coord or s_id not in subject_contig_coord:
                continue

            q_f = query_contig_coord[q_id] + q_f
            q_t = query_contig_coord[q_id] + q_t

            s_f = subject_contig_coord[s_id] + s_f
            s_t = subject_contig_coord[s_id] + s_t

            if strand == '+':
                ax.plot((s_f, s_t), (q_f, q_t), color, linewidth=linewidth)
            else:
                ax.plot((s_t, s_f), (q_f, q_t), color, linewidth=linewidth)

    def add_contig_grid(self, ax, query_contig_length_dict, subject_contig_length_dict, q_top=None, s_top=None, grid_colors='k', linewidths=0.5, q_contig_list=None, s_contig_list=None, rename_chr_map=None):
        query_contig_coord = {}
        subject_contig_coord = {}

        # for query aka y axis h
        q_hline_y_site = []
        q_tick_local = []
        q_tick_label = []
        q_num = 0
        q_top_num = 0

        if q_contig_list is None:
            q_contig_list = list(query_contig_length_dict.keys())

        for i in q_contig_list:
            q_top_num += 1
            if q_top and q_top_num > q_top:
                continue
            if q_top_num == 1:
                top_q_len = query_contig_length_dict[i]
            query_contig_coord[i] = q_num
            q_num += query_contig_length_dict[i]
            q_hline_y_site.append(q_num)
            q_tick_local.append(q_num - query_contig_length_dict[i]/2)
            if rename_chr_map:
                q_tick_label.append(rename_chr_map[i])
            else:
                q_tick_label.append(i)

        q_hline_y_site = q_hline_y_site[:-1]

        ax.hlines(q_hline_y_site, 0, 1, transform=ax.get_yaxis_transform(),
                  colors=grid_colors, linewidths=linewidths)

        # for subject aka x axis v
        s_vline_y_site = []
        s_tick_local = []
        s_tick_label = []
        s_num = 0
        s_top_num = 0

        if s_contig_list is None:
            s_contig_list = list(subject_contig_length_dict.keys())

        for i in s_contig_list:
            s_top_num += 1
            if s_top and s_top_num > s_top:
                continue
            if s_top_num == 1:
                top_s_len = subject_contig_length_dict[i]
            subject_contig_coord[i] = s_num
            s_num += subject_contig_length_dict[i]
            s_vline_y_site.append(s_num)
            s_tick_local.append(s_num - subject_contig_length_dict[i]/2)
            if rename_chr_map:
                s_tick_label.append(rename_chr_map[i])
            else:
                s_tick_label.append(i)

        s_vline_y_site = s_vline_y_site[:-1]

        ax.vlines(s_vline_y_site, 0, 1, transform=ax.get_xaxis_transform(),
                  colors=grid_colors, linewidths=linewidths)

        ax.invert_yaxis()

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.tick_params(axis='both', which='both', bottom=False, top=False,
                       left=False, right=False, labeltop=True, labelleft=True)

        ax.set_xticks(s_tick_local)
        ax.set_xticklabels(s_tick_label)
        ax.set_yticks(q_tick_local)
        ax.set_yticklabels(q_tick_label)

        ax.xaxis.set_tick_params(
            which='major', labelrotation=90, labeltop=True, labelbottom=False)

        x_y_lim = ((0, s_num), (q_num, 0))
        ax.set_xlim(x_y_lim[0])
        ax.set_ylim(x_y_lim[1])

        return query_contig_coord, subject_contig_coord


class GenomeSyntenyBlockJob(object):
    def __init__(self, sp1_id, sp1_gff, sp2_id=None, sp2_gff=None, gene_pair_file=None, sb_options=None, mcscan_output_file=None):
        self.sp1_id = sp1_id
        self.sp1_gff = sp1_gff
        self.sp2_id = sp2_id
        self.sp2_gff = sp2_gff
        self.gene_pair_file = gene_pair_file
        self.mcscan_output_file = mcscan_output_file

        self.sb_options = OrderedDict([
            ("min_size", 5),
            ("max_gap", 25),
            ("max_pvalue", 1),
            ("min_score", 50),
            ("gap_penality", -1),
            ("tandem_repeat_gap", 10)
        ])

        if sb_options:
            for i in sb_options:
                self.sb_options[i] = sb_options[i]

        self.sp1 = Genome(sp1_id, sp1_gff)
        if sp2_gff:
            self.sp2 = Genome(sp2_id, sp2_gff)
        else:
            self.sp2 = None

    def read_gene_pair(self, gene_pair_file, sp1, sp2=None):
        gene_pair_list = []
        with open(gene_pair_file, 'r') as f:
            for l in f:
                gene_id1, gene_id2 = l.strip().split()
                if sp2:
                    gp = GenePair(
                        sp1.gene_dict[gene_id1], sp2.gene_dict[gene_id2])
                    gene_pair_list.append(gp)
                else:
                    gp = GenePair(
                        sp1.gene_dict[gene_id1], sp1.gene_dict[gene_id2])
                    gene_pair_list.append(gp)
        return gene_pair_list

    def build_synteny_blocks(self, threads=8):
        self.gene_pair_list = self.read_gene_pair(
            self.gene_pair_file, self.sp1, self.sp2)

        sp1_chr_list = list(self.sp1.chr_dict.keys())
        if self.sp2:
            sp2_chr_list = list(self.sp2.chr_dict.keys())
            tmp_sp2_id = self.sp2_id
        else:
            sp2_chr_list = sp1_chr_list
            tmp_sp2_id = self.sp1_id

        sb_args = [self.sb_options[i] for i in self.sb_options]

        chr_gene_pair_list_dict = {}
        for q_chr in sp1_chr_list:
            for s_chr in sp2_chr_list:
                chr_gene_pair_list_dict[(q_chr, s_chr)] = []

        for gp in self.gene_pair_list:
            if gp.q_gene.sp_id == self.sp1_id and gp.s_gene.sp_id == tmp_sp2_id:
                chr_gene_pair_list_dict[(gp.q_gene.chr_id, gp.s_gene.chr_id)].append(
                    gp)
            elif gp.s_gene.sp_id == self.sp1_id and gp.q_gene.sp_id == tmp_sp2_id:
                chr_gene_pair_list_dict[(gp.s_gene.chr_id, gp.q_gene.chr_id)].append(
                    gp.reverse_myself())

        args_list = []
        args_id_list = []
        mlt_out = {}
        for q_chr in sp1_chr_list:
            for s_chr in sp2_chr_list:
                chr_gene_pair_list = chr_gene_pair_list_dict[(q_chr, s_chr)]
                # chr_gene_pair_list = []
                # for gp in self.gene_pair_list:
                #     if gp.q_gene.sp_id == self.sp1_id and gp.q_gene.chr_id == q_chr and gp.s_gene.sp_id == tmp_sp2_id and gp.s_gene.chr_id == s_chr:
                #         chr_gene_pair_list.append(gp)
                #     elif gp.s_gene.sp_id == self.sp1_id and gp.s_gene.chr_id == q_chr and gp.q_gene.sp_id == tmp_sp2_id and gp.q_gene.chr_id == s_chr:
                #         chr_gene_pair_list.append(gp.reverse_myself())
                if len(chr_gene_pair_list):
                    if threads == 1:
                        mlt_out[((self.sp1_id, q_chr), (tmp_sp2_id, s_chr))] = {}
                        mlt_out[((self.sp1_id, q_chr), (tmp_sp2_id, s_chr))]['output'] = get_synteny_block(
                            *tuple([chr_gene_pair_list] + sb_args))
                    args_list.append(tuple([chr_gene_pair_list] + sb_args))
                    args_id_list.append(
                        ((self.sp1_id, q_chr), (tmp_sp2_id, s_chr)))

        if threads > 1:
            mlt_out = multiprocess_running(
                get_synteny_block, args_list, threads, silence=False, args_id_list=args_id_list, timeout=None)
        self.synteny_blocks_dict = {i: mlt_out[i]['output'] for i in mlt_out}

        num = 0
        self.synteny_block_dict = OrderedDict()
        for chr_pair_info in self.synteny_blocks_dict:
            for sb_id in self.synteny_blocks_dict[chr_pair_info]:
                sb = self.synteny_blocks_dict[chr_pair_info][sb_id]
                self.synteny_block_dict[num] = sb
                num += 1

    def get_mcscan_parameter(self, mcscan_output_file):
        parameter_dict = OrderedDict()
        with open(mcscan_output_file, 'r') as f:
            for each_line in f:
                # statistics
                mobj = re.match(
                    r"# Number of collinear genes: (\d+), Percentage: (\d+\.\d+)", each_line)
                if mobj:
                    gene_in_coll, percentage = mobj.groups()
                    gene_in_coll, percentage = int(
                        gene_in_coll), float(percentage)

                mobj = re.match(r"# Number of all genes: (\d+)", each_line)
                if mobj:
                    all_gene = mobj.groups()[0]
                    all_gene = int(all_gene)

                # statistics wgdi xyx
                mobj = re.match(
                    r"# Number of collinear gene pairs: (\d+), Percentage: (\d+\.\d+)%", each_line)
                if mobj:
                    gene_in_coll, percentage = mobj.groups()
                    gene_in_coll, percentage = int(
                        gene_in_coll), float(percentage)

                mobj = re.match(
                    r"# Number of all gene pairs: (\d+)", each_line)
                if mobj:
                    all_gene = mobj.groups()[0]
                    all_gene = int(all_gene)

                # Parameters
                mobj = re.findall(r"^# (\S+): (\S+)$", each_line)
                if len(mobj) > 0:
                    p, v = mobj[0]
                    bad_flag = False
                    try:
                        v = float(v)
                    except:
                        bad_flag = True
                    if bad_flag is False:
                        parameter_dict[p] = v

        parameter_dict["gene_in_coll"] = gene_in_coll
        parameter_dict["percentage"] = percentage
        parameter_dict["all_gene"] = all_gene

        return parameter_dict

    def write_mcscan_output(self, mcscan_output_file):

        sb_gp_num = 0
        for i in self.synteny_block_dict:
            sb = self.synteny_block_dict[i]
            sb_gp_num += sb.property['gene_pair_num']

        with open(mcscan_output_file, 'w') as f:
            f.write("############### Parameters ###############\n# MIN_SIZE: %d\n# MAX_GAP: %d\n# MAX_PVALUE: %.2f\n# MIN_SCORE: %d\n# GAP_PENALITY: %d\n# TANDEM_REPEAT_GAP: %d\n" % tuple(
                [self.sb_options[i] for i in self.sb_options]))
            f.write("############### Statistics ###############\n# Number of collinear gene pairs: %d, Percentage: %.2f%%\n# Number of all gene pairs: %d\n##########################################\n" % (
                sb_gp_num, sb_gp_num/len(self.gene_pair_list)*100, len(self.gene_pair_list)))

            for num in self.synteny_block_dict:
                sb = self.synteny_block_dict[num]
                s = "## Alignment %d: score=%.1f e_value=%.3e N=%d %s&%s %s" % (
                    num, sb.property['score'], sb.property['p_value'], sb.property['gene_pair_num'], sb.q_chr, sb.s_chr, "+" if sb.strand == "+" else "-")
                f.write(s + "\n")
                for gp_id in sb.gene_pair_dict:
                    gp = sb.gene_pair_dict[gp_id]
                    s = "  %s-  %s:\t%s\t%s\t0" % (str(num),
                                                   str(gp_id), gp.q_gene.id, gp.s_gene.id)
                    f.write(s + "\n")

    def read_mcscan_output(self, mcscan_output_file=None, sp1_self_flag=False):
        if mcscan_output_file is None:
            mcscan_output_file = self.mcscan_output_file

        mcscan_parameter = self.get_mcscan_parameter(mcscan_output_file)

        self.synteny_block_dict = OrderedDict()

        with open(mcscan_output_file, 'r') as f:
            for each_line in f:
                # Block title
                mobj = re.match(
                    r"## Alignment (\S+): score=(\S+) e_value=(\S+) N=(\S+) (\S+)&(\S+) (\S+)", each_line)
                if mobj:
                    align_id, score, e_value, gene_pair_num, q_chr, s_chr, strand = mobj.groups()

                    align_id, score, e_value, gene_pair_num, q_chr, s_chr, strand = align_id, float(
                        score), float(e_value), int(gene_pair_num), q_chr, s_chr, strand
                    if strand == 'plus' or strand == '+':
                        strand = "+"
                    elif strand == 'minus' or strand == '-':
                        strand = "-"
                    else:
                        raise

                    property_dict = {
                        'score': score,
                        'e_value': e_value,
                        'gene_pair_num': gene_pair_num,
                    }

                    if sp1_self_flag:
                        self.synteny_block_dict[align_id] = SyntenyBlock(
                            align_id, self.sp1_id, self.sp1_id, strand, {}, property_dict, mcscan_parameter)
                    else:
                        self.synteny_block_dict[align_id] = SyntenyBlock(
                            align_id, self.sp1_id, self.sp2_id, strand, {}, property_dict, mcscan_parameter)

                # block line
                if re.match("^#", each_line):
                    continue
                else:
                    if align_id not in self.synteny_block_dict:
                        continue

                    align_id = each_line.split("-", 1)[0]
                    pair_id = each_line.split("-", 1)[1].split(":", 1)[0]

                    align_id = re.sub(r'\s+', '', align_id)
                    pair_id = int(re.sub(r'\s+', '', pair_id))

                    q_gene_id, s_gene_id, e_value = each_line.split(
                        "-", 1)[1].split(":", 1)[1].split()
                    align_id, pair_id, q_gene_id, s_gene_id, e_value = align_id, pair_id, q_gene_id, s_gene_id, float(
                        e_value)

                    if sp1_self_flag:
                        q_gene = self.sp1.gene_dict[q_gene_id]
                        s_gene = self.sp1.gene_dict[s_gene_id]
                    else:
                        q_gene = self.sp1.gene_dict[q_gene_id]
                        s_gene = self.sp2.gene_dict[s_gene_id]

                    property_dict = {'e_value': e_value}

                    self.synteny_block_dict[align_id].gene_pair_dict[pair_id] = GenePair(
                        q_gene, s_gene, property_dict)

        for align_id in self.synteny_block_dict:
            if sp1_self_flag:
                self.synteny_block_dict[align_id].get_full_info(
                    self.sp1, self.sp1)
            else:
                self.synteny_block_dict[align_id].get_full_info(
                    self.sp1, self.sp2)

    def get_sb_cover_dict(self):
        # merge block
        merged_synteny_block_dict = merge_blocks(
            self.synteny_block_dict, self.sp1, self.sp2)

        # get gene cover dict
        q_gene_covered_dict, q_range_loci_cover_chr_dict, q_range_base_cover_chr_dict = gene_cover_depth_stat(
            merged_synteny_block_dict, 'query', self.sp1)
        s_gene_covered_dict, s_range_loci_cover_chr_dict, s_range_base_cover_chr_dict = gene_cover_depth_stat(
            merged_synteny_block_dict, 'subject', self.sp2)

        self.cover_dict = {
            self.sp1_id: {
                'gene': q_gene_covered_dict,
                'loci': q_range_loci_cover_chr_dict,
                'base': q_range_base_cover_chr_dict,
            },
            self.sp2_id: {
                'gene': s_gene_covered_dict,
                'loci': s_range_loci_cover_chr_dict,
                'base': s_range_base_cover_chr_dict,
            }
        }

        self.merged_synteny_block_dict = merged_synteny_block_dict

    def plot(self, mode='base', save_file=None):

        self.get_sb_cover_dict()

        if mode == 'base':
            self.dot_plot = DotPlotJob(
                self.sp1, self.sp2, self.merged_synteny_block_dict, self.cover_dict[self.sp1_id]['base'], self.cover_dict[self.sp2_id]['base'])
            self.dot_plot.plot(save_file=save_file)
        elif mode == 'loci':
            self.dot_plot = DotPlotJob(
                self.sp1, self.sp2, self.merged_synteny_block_dict, sp1_loci_cover_dict=self.cover_dict[self.sp1_id]['loci'], sp2_loci_cover_dict=self.cover_dict[self.sp2_id]['loci'])
            self.dot_plot.plot(save_file=save_file, mode='loci')


if __name__ == '__main__':

    sp1_id = 'Cca'
    sp1_gff = '/lustre/home/xuyuxing/tmp/T49390N0.genome.gff3'
    sp2_id = 'Sly'
    sp2_gff = '/lustre/home/xuyuxing/tmp/T4081N0.genome.gff3'
    gene_pair_file = '/lustre/home/xuyuxing/tmp/mcscanx.homology'

    # build synteny blocks
    sb_job = GenomeSyntenyBlockJob(
        sp1_id, sp1_gff, sp2_id, sp2_gff, gene_pair_file)
    sb_job.build_synteny_blocks()

    mcscan_output_file = "/lustre/home/xuyuxing/tmp/mcscanx.collinearity"
    sb_job.write_mcscan_output(mcscan_output_file)

    # load synteny blocks

    sb_job = GenomeSyntenyBlockJob(
        sp1_id, sp1_gff, sp2_id, sp2_gff)
    sb_job.read_mcscan_output(mcscan_output_file)

    # test

    sp1_id = "Cgo"
    sp1_gff = "/lustre/home/xuyuxing/Work/orcidWGD2/WGD_identification/1.phylogenomics/gene_filter/Cgo.filter.gff3"
    sp2_id = "Gel"
    sp2_gff = "/lustre/home/xuyuxing/Work/orcidWGD2/WGD_identification/1.phylogenomics/gene_filter/Gel.filter.gff3"
    mcscan_output_file = "/lustre/home/xuyuxing/Work/orcidWGD2/WGD_identification/2.hWGD/mcscanxh/Cgo_vs_Gel_h/mcscanx.collinearity"

    sb_job = GenomeSyntenyBlockJob(
        sp1_id, sp1_gff, sp2_id, sp2_gff, mcscan_output_file=mcscan_output_file)

    sb_job.read_mcscan_output()
    sb_job.plot()
