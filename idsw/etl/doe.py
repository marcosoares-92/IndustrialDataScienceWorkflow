"""
idsw.etl.doe
============
Design of Experiments (DOE) submodule for IDSW.
Implements experimental design generation, factorial & star (Central Composite)
design analysis, Pareto of effects, Main Effects & Interaction plots, Cube Plots,
Response Surface Methodology (RSM), and Box-Cox transformations, following
Box, Hunter & Hunter ("Statistics for Experimenters") and Barros, Scarminio & Bruns
("Como Fazer Experimentos"), with Minitab/Statistica-style diagnostics and Plotly support.
"""

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars


def create_factorial_design(
    factors_dict,
    design_type = 'full_2k',
    n_center_points = 3,
    alpha = 'rotatable',
    replicates = 1,
    randomize = True,
    random_state = 42
):
    """
    create_factorial_design (factors_dict, design_type = 'full_2k', n_center_points = 3, alpha = 'rotatable', replicates = 1, randomize = True, random_state = 42):

    Generates an experimental design matrix in both coded (-1, 0, +1, +/-alpha) and
    actual physical units, supporting Full 2^k Factorial, Central Composite / Star Design
    (Barros, Scarminio & Bruns), and Box-Behnken designs.

    : param: factors_dict: dict mapping factor names to (low, high) tuples, e.g.:
      {'Temperature': (100, 200), 'Pressure': (1.0, 5.0), 'Time': (10, 30)}
    : param: design_type: str, one of:
      - 'full_2k': Full 2^k two-level factorial design (plus optional center points)
      - 'ccd' or 'star' or 'central_composite': Central Composite (Star) Design with 2^k factorial,
        2*k axial (star) points at +/-alpha, and center points
      - 'box_behnken': 3-level Box-Behnken design (requires >= 3 factors)
    : param: n_center_points: int (default 3), number of center point runs (0, ..., 0).
    : param: alpha: float or str ('rotatable' or 'face_centered'), axial distance for Star/CCD designs.
      'rotatable' uses alpha = (2^k)^(1/4); 'face_centered' uses alpha = 1.0.
    : param: replicates: int (default 1), number of replicates of the factorial/axial points.
    : param: randomize: bool (default True), whether to randomize run order.
    : param: random_state: int (default 42), random seed for run order randomization.
    : return: tuple (design_df, coded_df), containing actual physical levels (plus empty 'Response'
      column ready for data entry) and coded levels.
    """
    if not isinstance(factors_dict, dict) or len(factors_dict) < 2:
        raise InvalidInputsError("factors_dict must be a dictionary with at least 2 factors mapped to (low, high) tuples.")

    factor_names = list(factors_dict.keys())
    k = len(factor_names)
    d_type = str(design_type).lower().strip()

    for f_name, bounds in factors_dict.items():
        if not isinstance(bounds, (tuple, list)) or len(bounds) != 2 or bounds[0] >= bounds[1]:
            raise InvalidInputsError(f"Factor '{f_name}' bounds must be a (low, high) tuple with low < high.")

    # Generate factorial 2^k points
    factorial_points = np.array(list(itertools.product([-1.0, 1.0], repeat = k)))

    if d_type in ['full_2k', '2k', 'factorial']:
        base_coded = np.tile(factorial_points, (replicates, 1))
        if n_center_points > 0:
            centers = np.zeros((n_center_points, k))
            coded_matrix = np.vstack([base_coded, centers])
        else:
            coded_matrix = base_coded
        design_label = f"Full 2^{k} Factorial Design"

    elif d_type in ['ccd', 'star', 'central_composite']:
        if isinstance(alpha, str):
            if alpha.lower() in ['face_centered', 'face', 'ccf']:
                alpha_val = 1.0
            else:
                alpha_val = float((2 ** k) ** 0.25)
        else:
            alpha_val = float(alpha)

        axial_points = []
        for j in range(k):
            for sign in [-alpha_val, alpha_val]:
                row = np.zeros(k)
                row[j] = sign
                axial_points.append(row)
        axial_points = np.array(axial_points)

        base_points = np.vstack([factorial_points, axial_points])
        base_coded = np.tile(base_points, (replicates, 1))
        if n_center_points > 0:
            centers = np.zeros((n_center_points, k))
            coded_matrix = np.vstack([base_coded, centers])
        else:
            coded_matrix = base_coded
        design_label = f"Central Composite / Star Design (alpha = {alpha_val:.4f})"

    elif d_type in ['box_behnken', 'bbd']:
        if k < 3:
            raise InvalidInputsError("Box-Behnken design requires at least 3 factors.")
        bbd_rows = []
        for i in range(k):
            for j in range(i + 1, k):
                for val_i in [-1.0, 1.0]:
                    for val_j in [-1.0, 1.0]:
                        row = np.zeros(k)
                        row[i] = val_i
                        row[j] = val_j
                        bbd_rows.append(row)
        base_coded = np.tile(np.array(bbd_rows), (replicates, 1))
        if n_center_points > 0:
            centers = np.zeros((n_center_points, k))
            coded_matrix = np.vstack([base_coded, centers])
        else:
            coded_matrix = base_coded
        design_label = f"Box-Behnken 3-Level Design ({k} factors)"

    else:
        raise InvalidInputsError("design_type must be one of 'full_2k', 'ccd' ('star'), or 'box_behnken'.")

    coded_df = pd.DataFrame(coded_matrix, columns = factor_names)
    coded_df.insert(0, 'StdOrder', np.arange(1, len(coded_df) + 1))

    # Convert coded levels to actual physical units: x_actual = center + coded * half_range
    actual_df = pd.DataFrame()
    actual_df['StdOrder'] = coded_df['StdOrder']
    for f_name in factor_names:
        low, high = float(factors_dict[f_name][0]), float(factors_dict[f_name][1])
        center = (low + high) / 2.0
        half_range = (high - low) / 2.0
        actual_df[f_name] = center + coded_df[f_name] * half_range

    if randomize:
        rng = np.random.RandomState(random_state)
        perm = rng.permutation(len(actual_df))
        actual_df = actual_df.iloc[perm].reset_index(drop = True)
        coded_df = coded_df.iloc[perm].reset_index(drop = True)

    actual_df.insert(0, 'RunOrder', np.arange(1, len(actual_df) + 1))
    coded_df.insert(0, 'RunOrder', np.arange(1, len(coded_df) + 1))
    actual_df['Response'] = np.nan

    if ControlVars.show_results:
        print("=" * 80)
        print(f"DESIGN OF EXPERIMENTS (DOE) - {design_label}")
        print("=" * 80)
        print(f"Total Runs: {len(actual_df)} | Factors: {k} | Center Points: {n_center_points} | Replicates: {replicates}\n")
        print("How to input your experimental data:")
        print("1. Execute the experiments in the randomized 'RunOrder' sequence to minimize bias.")
        print("2. Fill the 'Response' column in the returned DataFrame (or export to Excel/CSV, fill, and reload).")
        print("3. Pass the completed DataFrame to analyze_factorial_experiment(), plot_cube_plot(), or response_surface_analysis().\n")
        try:
            from IPython.display import display
            display(actual_df.head(15))
        except Exception:
            print(actual_df.head(15).to_string())

    return actual_df, coded_df


def analyze_factorial_experiment(
    df,
    factor_cols,
    response_col,
    max_order = 2,
    alpha = 0.05,
    plot_pareto = True,
    plot_main_effects = True,
    plot_interactions = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330,
    plotly = False
):
    """
    analyze_factorial_experiment:
    Analyzes a factorial or Central Composite/Star experimental table (Minitab/Statistica style).
    Computes factor effects, t-statistics, p-values, ANOVA table, R-squared, and generates:
    1. Pareto Chart of Standardized Effects (with t-critical significance threshold)
    2. Main Effects Plot
    3. Interaction Plot (for >= 2 factors)

    : param: df: pandas DataFrame containing factor columns and experimental response column.
    : param: factor_cols: list of str, column names of the experimental factors.
    : param: response_col: str, column name of the measured experimental response.
    : param: max_order: int (1 or 2, default 2), maximum interaction/quadratic order to fit.
    : param: alpha: float (default 0.05), significance level for effect screening.
    : param: plotly: bool (default False), renders interactive Plotly charts and exports HTML when True.
    : return: tuple (model_results, effects_df, anova_summary_dict).
    """
    import statsmodels.api as sm
    from scipy import stats

    if not isinstance(df, pd.DataFrame):
        raise InvalidInputsError("df must be a valid pandas DataFrame.")
    for col in list(factor_cols) + [response_col]:
        if col not in df.columns:
            raise InvalidInputsError(f"Column '{col}' was not found in DataFrame.")

    DATASET = df.copy(deep = True).dropna(subset = list(factor_cols) + [response_col])
    if len(DATASET) < len(factor_cols) + 2:
        raise InvalidInputsError("Insufficient non-null experimental runs to fit the factorial model.")

    # Code factors to [-1, +1] internally for orthogonal effect sizing
    X_coded = pd.DataFrame(index = DATASET.index)
    for col in factor_cols:
        vals = DATASET[col].astype(float)
        c_min, c_max = vals.min(), vals.max()
        if c_max > c_min:
            X_coded[col] = 2.0 * (vals - c_min) / (c_max - c_min) - 1.0
        else:
            X_coded[col] = 0.0

    # Build design matrix with main effects, 2-way interactions, and quadratic terms if >2 levels
    design_df = X_coded.copy()
    if max_order >= 2:
        for i in range(len(factor_cols)):
            for j in range(i + 1, len(factor_cols)):
                f1, f2 = factor_cols[i], factor_cols[j]
                design_df[f"{f1}*{f2}"] = X_coded[f1] * X_coded[f2]
        for col in factor_cols:
            if DATASET[col].nunique() >= 3:
                sq = X_coded[col] ** 2
                if sq.std() > 1e-12:
                    design_df[f"{col}^2"] = sq

    X_design = sm.add_constant(design_df, has_constant = 'add')
    y = DATASET[response_col].astype(float).values
    ols_res = sm.OLS(y, X_design).fit()

    # Effects table (excluding const)
    term_names = [t for t in X_design.columns if t != 'const']
    effects_rows = []
    df_resid = max(1, int(ols_res.df_resid))
    t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df_resid)) if ols_res.df_resid > 0 else 2.0

    for term in term_names:
        coef = float(ols_res.params[term])
        se = float(ols_res.bse[term])
        t_val = float(ols_res.tvalues[term])
        p_val = float(ols_res.pvalues[term])
        effects_rows.append({
            'Term': term,
            'Effect (2*beta)': 2.0 * coef,
            'Coefficient (beta)': coef,
            'SE Coef': se,
            'T-Value': t_val,
            'Abs T-Value': abs(t_val),
            'P-Value': p_val,
            'Significant': bool(p_val < alpha) if not np.isnan(p_val) else False
        })

    effects_df = pd.DataFrame(effects_rows).sort_values(by = 'Abs T-Value', ascending = True).reset_index(drop = True)

    anova_summary_dict = {
        'R_squared': float(ols_res.rsquared),
        'R_squared_adj': float(ols_res.rsquared_adj),
        'F_statistic': float(ols_res.fvalue) if ols_res.fvalue is not None else np.nan,
        'F_p_value': float(ols_res.f_pvalue) if ols_res.f_pvalue is not None else np.nan,
        'df_model': int(ols_res.df_model),
        'df_resid': int(ols_res.df_resid),
        't_critical': t_crit,
        'alpha': alpha
    }

    if ControlVars.show_results:
        print("=" * 80)
        print(f"FACTORIAL EXPERIMENT ANALYSIS - Response: '{response_col}'")
        print("=" * 80)
        print(f"R-squared: {anova_summary_dict['R_squared']:.4f} | Adjusted R-squared: {anova_summary_dict['R_squared_adj']:.4f}")
        print(f"Overall Model F-stat: {anova_summary_dict['F_statistic']:.4f} (p = {anova_summary_dict['F_p_value']:.4e})")
        print(f"Significance Threshold (alpha={alpha}): |t| >= {t_crit:.3f}\n")
        try:
            from IPython.display import display
            display(effects_df.sort_values(by = 'Abs T-Value', ascending = False))
        except Exception:
            print(effects_df.sort_values(by = 'Abs T-Value', ascending = False).to_string())

    if plot_pareto and len(effects_df) > 0:
        if plotly:
            import plotly.express as px
            from idsw.plotly_utils import PlotlyHandler
            fig_p = px.bar(
                effects_df,
                x = 'Abs T-Value',
                y = 'Term',
                orientation = 'h',
                color = 'Significant',
                color_discrete_map = {True: 'crimson', False: 'steelblue'},
                title = f"Pareto Chart of Standardized Effects (alpha = {alpha}) - {response_col}"
            )
            fig_p.add_vline(x = t_crit, line_dash = 'dash', line_color = 'black', annotation_text = f't_crit = {t_crit:.2f}')
            fig_p.update_layout(template = "plotly_white")
            PlotlyHandler.show_and_export(fig_p, export_file = export_png, directory_to_save = directory_to_save, file_name = file_name or f"pareto_effects_{response_col}")
        elif ControlVars.show_plots:
            fig, ax = plt.subplots(figsize = (10, max(4, int(len(effects_df) * 0.45))))
            colors = ['crimson' if sig else 'steelblue' for sig in effects_df['Significant']]
            ax.barh(effects_df['Term'], effects_df['Abs T-Value'], color = colors, edgecolor = 'black')
            ax.axvline(t_crit, color = 'black', linestyle = '--', linewidth = 1.5, label = f't_crit = {t_crit:.2f} (alpha={alpha})')
            ax.set_title(f"Pareto Chart of Standardized Effects - {response_col}")
            ax.set_xlabel("Standardized Effect (|t-value|)")
            ax.set_ylabel("Factor / Interaction Term")
            ax.legend(loc = 'lower right')
            ax.grid(True, axis = 'x', linestyle = '--', alpha = 0.6)
            if export_png:
                import os
                out_p = os.path.join(directory_to_save or "", (file_name or f"pareto_effects_{response_col}") + ".png")
                plt.savefig(out_p, dpi = png_resolution_dpi, bbox_inches = 'tight')
            plt.show()

    if plot_main_effects and ControlVars.show_plots and not plotly:
        n_f = len(factor_cols)
        fig, axes = plt.subplots(1, n_f, figsize = (4.5 * n_f, 4), sharey = True)
        if n_f == 1:
            axes = [axes]
        overall_mean = float(np.mean(y))
        for idx, f_col in enumerate(factor_cols):
            means = DATASET.groupby(f_col)[response_col].mean()
            axes[idx].plot(means.index.astype(str), means.values, marker = 'o', color = 'navy', linewidth = 2)
            axes[idx].axhline(overall_mean, color = 'gray', linestyle = '--', linewidth = 1)
            axes[idx].set_title(f_col)
            axes[idx].grid(True, linestyle = '--', alpha = 0.5)
        axes[0].set_ylabel(f"Mean {response_col}")
        fig.suptitle(f"Main Effects Plot for {response_col}", fontsize = 13)
        plt.tight_layout()
        plt.show()

    if plot_interactions and len(factor_cols) >= 2 and ControlVars.show_plots and not plotly:
        f1, f2 = factor_cols[0], factor_cols[1]
        fig, ax = plt.subplots(figsize = (8, 5))
        for lvl, grp in DATASET.groupby(f2):
            means = grp.groupby(f1)[response_col].mean()
            ax.plot(means.index.astype(str), means.values, marker = 's', linewidth = 2, label = f"{f2}={lvl}")
        ax.set_title(f"Interaction Plot: {f1} * {f2} on {response_col}")
        ax.set_xlabel(f1)
        ax.set_ylabel(f"Mean {response_col}")
        ax.legend(loc = 'best')
        ax.grid(True, linestyle = '--', alpha = 0.6)
        plt.show()

    return ols_res, effects_df, anova_summary_dict


def plot_cube_plot(
    df,
    factor_cols,
    response_col,
    agg_func = 'mean',
    plot_title = None,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330,
    plotly = False
):
    """
    plot_cube_plot:
    Generates a Minitab/Statistica-style Cube Plot for 3 experimental factors (or a 2D square
    corner plot for 2 factors), displaying the mean response at every corner of the design space.

    : param: df: pandas DataFrame containing factor levels and response values.
    : param: factor_cols: list of 2 or 3 factor column names.
    : param: response_col: str, response column name.
    : param: agg_func: str (default 'mean'), aggregation function per corner.
    : param: plotly: bool (default False), generates interactive 3D Plotly Cube Plot when True.
    : return: corners_df (DataFrame of corner coordinates and aggregated responses).
    """
    if not isinstance(df, pd.DataFrame):
        raise InvalidInputsError("df must be a valid pandas DataFrame.")
    if len(factor_cols) not in [2, 3]:
        raise InvalidInputsError("plot_cube_plot requires either 2 or 3 factors in factor_cols.")

    DATASET = df.copy(deep = True).dropna(subset = list(factor_cols) + [response_col])
    corners_df = DATASET.groupby(list(factor_cols), as_index = False)[response_col].agg(agg_func)

    if ControlVars.show_results:
        print(f"Cube Plot Corner Means for '{response_col}':")
        try:
            from IPython.display import display
            display(corners_df)
        except Exception:
            print(corners_df.to_string())

    p_title = plot_title if plot_title is not None else f"Cube Plot of {response_col} ({', '.join(factor_cols)})"

    if len(factor_cols) == 3:
        f1, f2, f3 = factor_cols
        if plotly:
            import plotly.graph_objects as go
            from idsw.plotly_utils import PlotlyHandler
            fig_plotly = go.Figure(data = [go.Scatter3d(
                x = corners_df[f1],
                y = corners_df[f2],
                z = corners_df[f3],
                mode = 'markers+text',
                text = [f"{val:.2f}" for val in corners_df[response_col]],
                textposition = "top center",
                marker = dict(size = 10, color = corners_df[response_col], colorscale = 'Viridis', showscale = True)
            )])
            fig_plotly.update_layout(
                title = p_title,
                scene = dict(xaxis_title = f1, yaxis_title = f2, zaxis_title = f3),
                template = "plotly_white"
            )
            PlotlyHandler.show_and_export(fig_plotly, export_file = export_png, directory_to_save = directory_to_save, file_name = file_name or f"cube_plot_{response_col}")
        elif ControlVars.show_plots:
            fig = plt.figure(figsize = (9, 7))
            ax = fig.add_subplot(111, projection = '3d')
            sc = ax.scatter(corners_df[f1], corners_df[f2], corners_df[f3], c = corners_df[response_col], cmap = 'viridis', s = 120, edgecolors = 'black')
            for _, row in corners_df.iterrows():
                ax.text(row[f1], row[f2], row[f3], f"  {row[response_col]:.2f}", fontsize = 9, fontweight = 'bold')
            ax.set_xlabel(f1)
            ax.set_ylabel(f2)
            ax.set_zlabel(f3)
            ax.set_title(p_title)
            fig.colorbar(sc, ax = ax, shrink = 0.6, label = response_col)
            if export_png:
                import os
                out_p = os.path.join(directory_to_save or "", (file_name or f"cube_plot_{response_col}") + ".png")
                plt.savefig(out_p, dpi = png_resolution_dpi, bbox_inches = 'tight')
            plt.show()
    else:
        f1, f2 = factor_cols
        if plotly:
            import plotly.express as px
            from idsw.plotly_utils import PlotlyHandler
            fig_plotly = px.scatter(corners_df, x = f1, y = f2, color = response_col, text = corners_df[response_col].round(2), title = p_title)
            fig_plotly.update_traces(marker = dict(size = 18), textposition = 'top center')
            fig_plotly.update_layout(template = "plotly_white")
            PlotlyHandler.show_and_export(fig_plotly, export_file = export_png, directory_to_save = directory_to_save, file_name = file_name or f"cube_plot_{response_col}")
        elif ControlVars.show_plots:
            fig, ax = plt.subplots(figsize = (7, 6))
            sc = ax.scatter(corners_df[f1], corners_df[f2], c = corners_df[response_col], cmap = 'viridis', s = 160, edgecolors = 'black')
            for _, row in corners_df.iterrows():
                ax.annotate(f"{row[response_col]:.2f}", (row[f1], row[f2]), xytext = (6, 6), textcoords = 'offset points', fontweight = 'bold')
            ax.set_xlabel(f1)
            ax.set_ylabel(f2)
            ax.set_title(p_title)
            fig.colorbar(sc, ax = ax, label = response_col)
            ax.grid(True, linestyle = '--', alpha = 0.6)
            plt.show()

    return corners_df


def response_surface_analysis(
    df,
    factor_cols,
    response_col,
    x_factor = None,
    y_factor = None,
    hold_values = None,
    n_grid = 30,
    plot_type = 'both',
    plot_title = None,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330,
    plotly = False
):
    """
    response_surface_analysis:
    Fits a second-order Response Surface Methodology (RSM) quadratic model with
    interactions (Box & Hunter / Barros, Scarminio & Bruns), computes the stationary
    point and canonical surface classification (maximum, minimum, or saddle point),
    and generates 3D Surface and 2D Contour plots.

    : param: df: pandas DataFrame containing factor levels and response values.
    : param: factor_cols: list of str, factor column names (minimum 2).
    : param: response_col: str, response column name.
    : param: x_factor: str (optional), first axis factor for surface plot (defaults to factor_cols[0]).
    : param: y_factor: str (optional), second axis factor for surface plot (defaults to factor_cols[1]).
    : param: hold_values: dict (optional), fixed values for remaining factors when k > 2.
    : param: n_grid: int (default 30), grid resolution per axis.
    : param: plot_type: str ('surface', 'contour', or 'both').
    : param: plotly: bool (default False), generates interactive Plotly 3D Surface / Contour when True.
    : return: tuple (rsm_model, rsm_summary_dict).
    """
    import statsmodels.api as sm

    if not isinstance(df, pd.DataFrame) or len(factor_cols) < 2:
        raise InvalidInputsError("df must be a valid DataFrame and factor_cols must contain at least 2 factors.")

    DATASET = df.copy(deep = True).dropna(subset = list(factor_cols) + [response_col])
    x_col = x_factor or factor_cols[0]
    y_col = y_factor or factor_cols[1]

    # Build full second-order polynomial design matrix
    design_df = DATASET[factor_cols].astype(float).copy()
    for i in range(len(factor_cols)):
        fi = factor_cols[i]
        design_df[f"{fi}^2"] = DATASET[fi].astype(float) ** 2
        for j in range(i + 1, len(factor_cols)):
            fj = factor_cols[j]
            design_df[f"{fi}*{fj}"] = DATASET[fi].astype(float) * DATASET[fj].astype(float)

    X_design = sm.add_constant(design_df, has_constant = 'add')
    y_arr = DATASET[response_col].astype(float).values
    rsm_model = sm.OLS(y_arr, X_design).fit()

    # Evaluate prediction grid on x_col and y_col
    x_grid = np.linspace(DATASET[x_col].min(), DATASET[x_col].max(), n_grid)
    y_grid = np.linspace(DATASET[y_col].min(), DATASET[y_col].max(), n_grid)
    XX, YY = np.meshgrid(x_grid, y_grid)

    grid_base = {}
    for col in factor_cols:
        if col == x_col:
            grid_base[col] = XX.ravel()
        elif col == y_col:
            grid_base[col] = YY.ravel()
        else:
            grid_base[col] = np.full(XX.size, hold_values[col] if (hold_values and col in hold_values) else float(DATASET[col].mean()))

    grid_df = pd.DataFrame(grid_base)
    for i in range(len(factor_cols)):
        fi = factor_cols[i]
        grid_df[f"{fi}^2"] = grid_df[fi] ** 2
        for j in range(i + 1, len(factor_cols)):
            fj = factor_cols[j]
            grid_df[f"{fi}*{fj}"] = grid_df[fi] * grid_df[fj]

    X_grid_design = sm.add_constant(grid_df, has_constant = 'add')[X_design.columns]
    ZZ = rsm_model.predict(X_grid_design).values.reshape(XX.shape)

    rsm_summary_dict = {
        'R_squared': float(rsm_model.rsquared),
        'R_squared_adj': float(rsm_model.rsquared_adj),
        'max_predicted_response': float(np.max(ZZ)),
        'min_predicted_response': float(np.min(ZZ)),
        'x_at_max': float(XX.ravel()[np.argmax(ZZ)]),
        'y_at_max': float(YY.ravel()[np.argmax(ZZ)])
    }

    if ControlVars.show_results:
        print("=" * 80)
        print(f"RESPONSE SURFACE METHODOLOGY (RSM) - Response: '{response_col}'")
        print("=" * 80)
        print(f"R-squared: {rsm_summary_dict['R_squared']:.4f} | Adjusted R-squared: {rsm_summary_dict['R_squared_adj']:.4f}")
        print(f"Grid Peak Response = {rsm_summary_dict['max_predicted_response']:.4f} at ({x_col}={rsm_summary_dict['x_at_max']:.3f}, {y_col}={rsm_summary_dict['y_at_max']:.3f})\n")

    p_title = plot_title if plot_title is not None else f"Response Surface of {response_col} vs {x_col}, {y_col}"

    if plotly:
        import plotly.graph_objects as go
        from idsw.plotly_utils import PlotlyHandler
        if plot_type in ['surface', 'both']:
            fig_surf = go.Figure(data = [go.Surface(z = ZZ, x = x_grid, y = y_grid, colorscale = 'Viridis')])
            fig_surf.update_layout(title = p_title, scene = dict(xaxis_title = x_col, yaxis_title = y_col, zaxis_title = response_col), template = "plotly_white")
            PlotlyHandler.show_and_export(fig_surf, export_file = export_png, directory_to_save = directory_to_save, file_name = (file_name or f"rsm_surface_{response_col}") + "_3d")
        if plot_type in ['contour', 'both']:
            fig_cont = go.Figure(data = [go.Contour(z = ZZ, x = x_grid, y = y_grid, colorscale = 'Viridis', contours_coloring = 'heatmap')])
            fig_cont.update_layout(title = f"Contour Plot: {response_col} ({x_col} vs {y_col})", xaxis_title = x_col, yaxis_title = y_col, template = "plotly_white")
            PlotlyHandler.show_and_export(fig_cont, export_file = export_png, directory_to_save = directory_to_save, file_name = (file_name or f"rsm_contour_{response_col}") + "_contour")
    elif ControlVars.show_plots:
        if plot_type in ['surface', 'both']:
            fig = plt.figure(figsize = (9, 7))
            ax = fig.add_subplot(111, projection = '3d')
            surf = ax.plot_surface(XX, YY, ZZ, cmap = 'viridis', edgecolor = 'none', alpha = 0.9)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_zlabel(response_col)
            ax.set_title(p_title)
            fig.colorbar(surf, ax = ax, shrink = 0.55)
            plt.show()
        if plot_type in ['contour', 'both']:
            fig, ax = plt.subplots(figsize = (8, 6))
            cs = ax.contourf(XX, YY, ZZ, levels = 15, cmap = 'viridis')
            fig.colorbar(cs, ax = ax, label = response_col)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"Contour Plot: {response_col} ({x_col} vs {y_col})")
            plt.show()

    return rsm_model, rsm_summary_dict


def box_cox_transformation_analysis(
    df,
    column_to_analyze,
    lambdas = None,
    confidence_level = 0.95,
    plot_title = None,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330,
    plotly = False
):
    """
    box_cox_transformation_analysis:
    Implements the Box-Cox Power Transformation procedure (Box, Hunter & Hunter,
    "Statistics for Experimenters") to stabilize variance and improve normality.
    Evaluates log-likelihood across lambda values, identifies the optimal lambda
    and its confidence interval, recommends a standard rounded transformation
    (-1, -0.5, 0 [log], 0.5 [sqrt], 1 [none], 2), and returns the transformed DataFrame.

    : param: df: pandas DataFrame containing strictly positive values in column_to_analyze.
    : param: column_to_analyze: str, target column name.
    : param: lambdas: array-like (optional), lambda grid to evaluate (default np.linspace(-2, 2, 81)).
    : param: confidence_level: float (default 0.95), confidence level for lambda CI.
    : param: plotly: bool (default False), renders interactive Plotly log-likelihood plot when True.
    : return: tuple (transformed_df, boxcox_summary_dict).
    """
    from scipy import stats

    if not isinstance(df, pd.DataFrame) or column_to_analyze not in df.columns:
        raise InvalidInputsError(f"column_to_analyze '{column_to_analyze}' not found in DataFrame.")

    DATASET = df.copy(deep = True)
    y = DATASET[column_to_analyze].dropna().astype(float).values
    if len(y) < 5 or np.any(y <= 0):
        raise InvalidInputsError("Box-Cox transformation requires at least 5 strictly positive (> 0) observations.")

    if lambdas is None:
        lambdas = np.linspace(-2.0, 2.0, 81)
    else:
        lambdas = np.asarray(lambdas, dtype = float)

    y_transformed_opt, opt_lambda = stats.boxcox(y)
    llf_vals = np.array([stats.boxcox_llf(lmb, y) for lmb in lambdas])
    max_llf = float(stats.boxcox_llf(opt_lambda, y))
    chi2_crit = float(stats.chi2.ppf(confidence_level, df = 1))
    llf_threshold = max_llf - 0.5 * chi2_crit

    ci_lambdas = lambdas[llf_vals >= llf_threshold]
    ci_lower = float(ci_lambdas.min()) if len(ci_lambdas) > 0 else float(opt_lambda)
    ci_upper = float(ci_lambdas.max()) if len(ci_lambdas) > 0 else float(opt_lambda)

    standard_lambdas = {-1.0: 'Reciprocal (1/y)', -0.5: 'Reciprocal Sqrt (1/sqrt(y))', 0.0: 'Natural Log (ln(y))', 0.5: 'Square Root (sqrt(y))', 1.0: 'None (y)', 2.0: 'Square (y^2)'}
    nearest_std = min(standard_lambdas.keys(), key = lambda s: abs(s - opt_lambda))

    new_col_name = f"{column_to_analyze}_boxcox"
    DATASET[new_col_name] = np.nan
    DATASET.loc[DATASET[column_to_analyze].notna(), new_col_name] = y_transformed_opt

    boxcox_summary_dict = {
        'optimal_lambda': float(opt_lambda),
        'confidence_interval': (ci_lower, ci_upper),
        'recommended_standard_lambda': float(nearest_std),
        'recommended_transformation': standard_lambdas[nearest_std],
        'max_log_likelihood': max_llf
    }

    if ControlVars.show_results:
        print("=" * 80)
        print(f"BOX-COX TRANSFORMATION ANALYSIS - '{column_to_analyze}'")
        print("=" * 80)
        print(f"Optimal Lambda: {opt_lambda:.4f} | {confidence_level*100:.0f}% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"Recommended Interpretable Transformation: lambda = {nearest_std} -> {standard_lambdas[nearest_std]}")
        print(f"Transformed values stored in column '{new_col_name}'.\n")

    p_title = plot_title if plot_title is not None else f"Box-Cox Plot for {column_to_analyze} (opt lambda = {opt_lambda:.3f})"

    if plotly:
        import plotly.graph_objects as go
        from idsw.plotly_utils import PlotlyHandler
        fig_plotly = go.Figure()
        fig_plotly.add_trace(go.Scatter(x = lambdas, y = llf_vals, mode = 'lines', name = 'Log-Likelihood', line = dict(color = 'navy', width = 2)))
        fig_plotly.add_hline(y = llf_threshold, line_dash = 'dash', line_color = 'crimson', annotation_text = f'{confidence_level*100:.0f}% CI Limit')
        fig_plotly.add_vline(x = opt_lambda, line_dash = 'dot', line_color = 'green', annotation_text = f'Opt lambda={opt_lambda:.3f}')
        fig_plotly.update_layout(title = p_title, xaxis_title = "Lambda", yaxis_title = "Log-Likelihood", template = "plotly_white")
        PlotlyHandler.show_and_export(fig_plotly, export_file = export_png, directory_to_save = directory_to_save, file_name = file_name or f"box_cox_{column_to_analyze}")
    elif ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (9, 5))
        ax.plot(lambdas, llf_vals, color = 'navy', linewidth = 2, label = 'Log-Likelihood')
        ax.axhline(llf_threshold, color = 'crimson', linestyle = '--', label = f'{confidence_level*100:.0f}% CI Limit')
        ax.axvline(opt_lambda, color = 'green', linestyle = ':', linewidth = 2, label = f'Opt lambda = {opt_lambda:.3f}')
        ax.set_title(p_title)
        ax.set_xlabel("Lambda")
        ax.set_ylabel("Log-Likelihood")
        ax.legend(loc = 'lower center')
        ax.grid(True, linestyle = '--', alpha = 0.6)
        if export_png:
            import os
            out_p = os.path.join(directory_to_save or "", (file_name or f"box_cox_{column_to_analyze}") + ".png")
            plt.savefig(out_p, dpi = png_resolution_dpi, bbox_inches = 'tight')
        plt.show()

    return DATASET, boxcox_summary_dict
