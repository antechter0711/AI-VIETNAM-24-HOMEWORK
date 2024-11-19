# -*- coding: utf-8 -*-
"""Softmax Regression

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13lMzFCUrqj4pHiC2FX68WZ8lnvg7Ksd6
"""

import pandas as pd

def analyze_sales(df):
    """
    Analyze sales data from a DataFrame containing month, revenue, and cost columns.
    Returns a DataFrame with additional analysis including margins and cost trends.

    Parameters:
    df (pandas.DataFrame): DataFrame with columns 'month', 'revenue', and 'cost'

    Returns:
    pandas.DataFrame: Original data with additional analysis columns
    """
    # Create a copy to avoid modifying the original DataFrame
    analysis = df.copy()

    # Calculate margin (profit) in dollars
    analysis['margin'] = analysis['revenue'] - analysis['cost']

    # Calculate margin percentage
    analysis['margin_percentage'] = (analysis['margin'] / analysis['revenue'] * 100).round(2)

    # Calculate month-over-month revenue growth
    analysis['revenue_growth'] = analysis['revenue'].pct_change() * 100

    # Calculate month-over-month cost changes
    analysis['cost_growth'] = analysis['cost'].pct_change() * 100

    # Calculate cost as percentage of revenue
    analysis['cost_to_revenue_ratio'] = (analysis['cost'] / analysis['revenue'] * 100).round(2)

    # Add summary statistics
    summary = {
        'total_revenue': analysis['revenue'].sum(),
        'total_cost': analysis['cost'].sum(),
        'total_margin': analysis['margin'].sum(),
        'average_margin_percentage': analysis['margin_percentage'].mean(),
        'average_cost_to_revenue': analysis['cost_to_revenue_ratio'].mean(),
        'highest_cost_month': analysis.loc[analysis['cost'].idxmax(), 'month'],
        'lowest_cost_month': analysis.loc[analysis['cost'].idxmin(), 'month'],
        'highest_cost_growth': analysis['cost_growth'].max(),
        'average_cost_growth': analysis['cost_growth'].mean(),
        'best_margin_month': analysis.loc[analysis['margin'].idxmax(), 'month'],
        'worst_margin_month': analysis.loc[analysis['margin'].idxmin(), 'month']
    }

    return analysis, summary