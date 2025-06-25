import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix


def create_plots(df: pd.DataFrame, out_dir: str = 'plots') -> None:
    """
    Generate and save a suite of EDA plots for a DataFrame.

    Plots:
      - Histograms for numeric columns
      - Boxplots for numeric columns
      - Correlation matrix heatmap
      - Scatter matrix for up to 6 numeric columns
      - Bar plots for top categories in object columns
    """
    # Ensure output directory exists
    output_path = Path(out_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Select numeric and categorical columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # 1. Histograms
    for col in numeric_cols:
        plt.figure()
        df[col].hist()
        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(output_path / f'{col}_hist.png')
        plt.close()

    # 2. Boxplots
    for col in numeric_cols:
        plt.figure()
        df.boxplot(column=col)
        plt.title(f'Boxplot of {col}')
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(output_path / f'{col}_box.png')
        plt.close()

    # 3. Correlation Heatmap
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        plt.figure()
        plt.imshow(corr, aspect='auto')
        plt.colorbar()
        plt.xticks(range(len(corr)), corr.columns, rotation=90)
        plt.yticks(range(len(corr)), corr.index)
        plt.title('Correlation Matrix Heatmap')
        plt.tight_layout()
        plt.savefig(output_path / 'correlation_matrix.png')
        plt.close()

    # 4. Scatter Matrix (Pairplot)
    if len(numeric_cols) >= 2:
        subset = numeric_cols[:6]  # limit to first 6 for readability
        sm = scatter_matrix(df[subset], diagonal='hist', figsize=(8, 8))
        # Save the figure containing all axes
        fig = plt.gcf()
        fig.suptitle('Scatter Matrix')
        plt.tight_layout()
        fig_path = output_path / 'scatter_matrix.png'
        fig.savefig(fig_path)
        plt.close(fig)

    # 5. Bar Plots for Top Categories
    for col in categorical_cols:
        counts = df[col].value_counts().nlargest(10)
        plt.figure()
        counts.plot(kind='bar')
        plt.title(f'Top Categories in {col}')
        plt.xlabel(col)
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(output_path / f'{col}_bar.png')
        plt.close()

    print(f"Plots saved in directory: {output_path.resolve()}")
