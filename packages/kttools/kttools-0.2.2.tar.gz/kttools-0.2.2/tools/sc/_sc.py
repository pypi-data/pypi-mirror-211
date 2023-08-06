#!/usr/bin/env python
# @Author: Kelvin
# @Date:   2022-07-18 11:33:46
# @Last Modified by:   Kelvin
# @Last Modified time: 2022-11-17 16:09:57
"""Miscellaneous single-cell functions."""
import functools
import math

import numpy as np
import scanpy as sc
import pandas as pd

from pandas import DataFrame
from anndata import AnnData

from typing import List, Union


def exportDEres(
    adata: AnnData,
    column: str = None,
    filename: str = None,
    remove_mito_ribo: bool = True,
    key: str = "rank_genes_groups",
) -> DataFrame:
    """
    Export DE results from scanpy.

    Parameters
    ----------
    adata : AnnData
        AnnData object with `sc.tl.rank_genes_groups` performed.
    column : Optional[str], optional
        specific contrast to return.
    filename : Optional[str], optional
        if provided, save as file. Otherwise, return as DataFrame.
    remove_mito_ribo : bool, optional
        whether to filter all mito and ribo genes in the output.
    key : str, optional
        name in `.uns` to retrieve DE results.

    Returns
    -------
    DataFrame
        `DataFrame` of DE results.
    """
    if column is None:
        column = list(adata.uns[key]["scores"].dtype.fields.keys())[0]
    else:
        column = column

    if filename is not None:
        df_final = returnDEres(
            adata,
            column=column,
            remove_mito_ribo=remove_mito_ribo,
            key=key,
        )
        df_final.to_csv(filename, sep="\t")
    else:
        df = returnDEres(
            adata,
            column=column,
            remove_mito_ribo=remove_mito_ribo,
            key=key,
        )
        return df


def returnDEres(
    adata: AnnData,
    column: str = None,
    remove_mito_ribo: bool = True,
    key: str = "rank_genes_groups",
) -> DataFrame:
    """Summary

    Parameters
    ----------
    adata : AnnData
        AnnData object with `sc.tl.rank_genes_groups` performed.
    column : Optional[str], optional
        specific contrast to return.
    remove_mito_ribo : bool, optional
        whether to filter all mito and ribo genes in the output.
    key : str, optional
        name in `.uns` to retrieve DE results.

    Returns
    -------
    DataFrame
        `DataFrame` of DE results.
    """
    if key is None:
        key = "rank_genes_groups"
    else:
        key = key

    if column is None:
        column = list(adata.uns[key]["scores"].dtype.fields.keys())[0]
    else:
        column = column
    reference = adata.uns["rank_genes_groups"]["params"]["reference"]

    scores = DataFrame(
        data=adata.uns[key]["scores"][column], index=adata.uns[key]["names"][column]
    )
    lfc = DataFrame(
        data=adata.uns[key]["logfoldchanges"][column],
        index=adata.uns[key]["names"][column],
    )
    pvals = DataFrame(
        data=adata.uns[key]["pvals"][column], index=adata.uns[key]["names"][column]
    )
    padj = DataFrame(
        data=adata.uns[key]["pvals_adj"][column], index=adata.uns[key]["names"][column]
    )
    try:
        pts = DataFrame(
            data=adata.uns[key]["pts"][column], index=adata.uns[key]["names"][column]
        )
        ptsx = DataFrame(
            data=adata.uns[key]["pts_" + reference][column],
            index=adata.uns[key]["names"][column],
        )
    except:
        pass
    scores = scores.loc[scores.index.dropna()]
    lfc = lfc.loc[lfc.index.dropna()]
    pvals = pvals.loc[pvals.index.dropna()]
    padj = padj.loc[padj.index.dropna()]
    try:
        pts = pts.loc[pts.index.dropna()]
        ptsx = ptsx.loc[ptsx.index.dropna()]
    except:
        pass
    try:
        dfs = [scores, lfc, pvals, padj, pts, ptsx]
    except:
        dfs = [scores, lfc, pvals, padj]
    df_final = functools.reduce(
        lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
        dfs,
    )
    try:
        df_final.columns = [
            "scores",
            "logfoldchanges",
            "pvals",
            "pvals_adj",
            "pts" + "_" + column,
            "pts_" + reference,
        ]
    except:
        df_final.columns = ["scores", "logfoldchanges", "pvals", "pvals_adj"]
    if remove_mito_ribo:
        df_final = df_final[
            ~df_final.index.isin(
                list(df_final.filter(regex="^RPL|^RPS|^MRPS|^MRPL|^MT-", axis=0).index)
            )
        ]
        df_final = df_final[
            ~df_final.index.isin(
                list(df_final.filter(regex="^Rpl|^Rps|^Mrps|^Mrpl|^mt-", axis=0).index)
            )
        ]

    return df_final


def vmax(adata: AnnData, genes: Union[List, str], pct: float) -> List:
    """
    Extract the maximum expression value from list of genes in `AnnData` at the specified `pct`.

    Parameters
    ----------
    adata : AnnData
        input `AnnData` object.
    genes : Union[List, str]
        gene(s) to query from `AnnData` object.
    pct : float
        percentage to cut-off and return.

    Returns
    -------
    List
        List of maximum values.
    """
    if type(genes) is not list:
        genes = [genes]
    vm = []
    for g in genes:
        try:
            idx = adata.raw.var.index.get_loc(g)
        except:
            idx = adata.var.index.get_loc(g)
        vm.append(
            math.ceil(np.quantile(adata.raw.X[:, idx].toarray(), pct) * 100.0) / 100.0
        )
    return vm


def vmin(adata: AnnData, genes: Union[List, str], pct: float) -> List:
    """
    Extract the minimum expression value from list of genes in `AnnData` at the specified `pct`.

    Parameters
    ----------
    adata : AnnData
        input `AnnData` object.
    genes : Union[List, str]
        gene(s) to query from `AnnData` object.
    pct : float
        percentage to cut-off and return.

    Returns
    -------
    List
        List of minimum values.
    """
    if type(genes) is not list:
        genes = [genes]
    vm = []
    for g in genes:
        try:
            idx = adata.raw.var.index.get_loc(g)
        except:
            idx = adata.var.index.get_loc(g)
        vm.append(
            math.ceil(np.quantile(adata.raw.X[:, idx].toarray(), 1 - pct) * 100.0)
            / 100.0
        )
    return vm


def cell_cycle_scoring(adata: AnnData, human: bool = False):
    """
    Run cell cycle scoring on `AnnData` object.

    Parameters
    ----------
    adata : AnnData
        input `AnnData` object.
    human : bool, optional
        whether the data is human or not (mouse).

    """
    # cell cycle scoring
    adata_cc = adata.copy()
    if adata_cc.raw is not None:
        adata_cc = adata_cc.raw.to_adata()

    if float(np.max(adata_cc.X)).is_integer():
        # raw integer counts
        sc.pp.normalize_total(adata_cc, target_sum=1e4)
        sc.pp.log1p(adata_cc)
        sc.pp.scale(adata_cc)
    elif np.min(adata_cc.X) == 0:
        if "log1p" not in adata_cc.uns:
            sc.pp.log1p(adata_cc)
        # not scaled
        sc.pp.scale(adata_cc)
    else:
        raise ValueError("Please provide either raw integer or normalised data.")

    if not human:
        s_genes = [
            "Mcm5",
            "Pcna",
            "Tyms",
            "Fen1",
            "Mcm2",
            "Mcm4",
            "Rrm1",
            "Ung",
            "Gins2",
            "Mcm6",
            "Cdca7",
            "Dtl",
            "Prim1",
            "Uhrf1",
            "Hells",
            "Rfc2",
            "Rpa2",
            "Nasp",
            "Rad51ap1",
            "Gmnn",
            "Wdr76",
            "Slbp",
            "Ccne2",
            "Msh2",
            "Rad51",
            "Rrm2",
            "Cdc45",
            "Cdc6",
            "Exo1",
            "Tipin",
            "Dscc1",
            "Blm",
            "Casp8ap2",
            "Usp1",
            "Clspn",
            "Pola1",
            "Chaf1b",
            "Brip1",
            "E2f8",
        ]
        g2m_genes = [
            "Hmgb2",
            "Cdk1",
            "Nusap1",
            "Ube2c",
            "Birc5",
            "Tpx2",
            "Top2a",
            "Ndc80",
            "Cks2",
            "Nuf2",
            "Cks1b",
            "Mki67",
            "Tmpo",
            "Cenpf",
            "Tacc3",
            "Smc4",
            "Ccnb2",
            "Ckap2l",
            "Ckap2",
            "Aurkb",
            "Bub1",
            "Kif11",
            "Anp32e",
            "Tubb4b",
            "Gtse1",
            "Kif20b",
            "Hjurp",
            "Cdca3",
            "Cdc20",
            "Ttk",
            "Cdc25c",
            "Kif2c",
            "Rangap1",
            "Ncapd2",
            "Dlgap5",
            "Cdca2",
            "Cdca8",
            "Ect2",
            "Kif23",
            "Hmmr",
            "Aurka",
            "Psrc1",
            "Anln",
            "Lbr",
            "Ckap5",
            "Cenpe",
            "Ctcf",
            "Nek2",
            "G2e3",
            "Gas2l3",
            "Cbx5",
            "Cenpa",
        ]
    else:
        s_genes = [
            "MCM5",
            "PCNA",
            "TYMS",
            "FEN1",
            "MCM2",
            "MCM4",
            "RRM1",
            "UNG",
            "GINS2",
            "MCM6",
            "CDCA7",
            "DTL",
            "PRIM1",
            "UHRF1",
            "MLF1IP",
            "HELLS",
            "RFC2",
            "RPA2",
            "NASP",
            "RAD51AP1",
            "GMNN",
            "WDR76",
            "SLBP",
            "CCNE2",
            "UBR7",
            "POLD3",
            "MSH2",
            "ATAD2",
            "RAD51",
            "RRM2",
            "CDC45",
            "CDC6",
            "EXO1",
            "TIPIN",
            "DSCC1",
            "BLM",
            "CASP8AP2",
            "USP1",
            "CLSPN",
            "POLA1",
            "CHAF1B",
            "BRIP1",
            "E2F8",
        ]
        g2m_genes = [
            "HMGB2",
            "CDK1",
            "NUSAP1",
            "UBE2C",
            "BIRC5",
            "TPX2",
            "TOP2A",
            "NDC80",
            "CKS2",
            "NUF2",
            "CKS1B",
            "MKI67",
            "TMPO",
            "CENPF",
            "TACC3",
            "FAM64A",
            "SMC4",
            "CCNB2",
            "CKAP2L",
            "CKAP2",
            "AURKB",
            "BUB1",
            "KIF11",
            "ANP32E",
            "TUBB4B",
            "GTSE1",
            "KIF20B",
            "HJURP",
            "CDCA3",
            "HN1",
            "CDC20",
            "TTK",
            "CDC25C",
            "KIF2C",
            "RANGAP1",
            "NCAPD2",
            "DLGAP5",
            "CDCA2",
            "CDCA8",
            "ECT2",
            "KIF23",
            "HMMR",
            "AURKA",
            "PSRC1",
            "ANLN",
            "LBR",
            "CKAP5",
            "CENPE",
            "CTCF",
            "NEK2",
            "G2E3",
            "GAS2L3",
            "CBX5",
            "CENPA",
        ]
    sc.tl.score_genes_cell_cycle(
        adata_cc, s_genes=s_genes, g2m_genes=g2m_genes, use_raw=False
    )
    for x in ["S_score", "G2M_score", "phase"]:
        adata.obs[x] = adata_cc.obs[x]


def combine_two_categories(adata: AnnData, A: str, B: str, sep: str = "_") -> None:
    """Combine two categories in place, respecting the order of the concatenation.

    Parameters
    ----------
    adata : AnnData
        Input anndata object.
    A : str
        Column name for first category.
    B : str
        Column name for second category.
    sep : str, optional
        The separator to combine the names.
    """
    comb_cat = A + sep + B
    adata.obs[comb_cat] = [a + "_" + b for a, b in zip(adata.obs[A], adata.obs[B])]
    adata.obs[A] = adata.obs[A].astype("category")
    adata.obs[B] = adata.obs[B].astype("category")
    a_cat = adata.obs[A].cat.categories
    b_cat = adata.obs[B].cat.categories
    cats = []
    for a in a_cat:
        for b in b_cat:
            cats.append(a + "_" + b)
    adata.obs[comb_cat] = adata.obs[comb_cat].astype("category")
    adata.obs[comb_cat] = adata.obs[comb_cat].cat.reorder_categories(
        [c for c in cats if c in adata.obs[comb_cat].cat.categories]
    )
