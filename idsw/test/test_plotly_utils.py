import unittest
import os
import tempfile
import numpy as np
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from idsw import ControlVars
from idsw.plotly_utils import PlotlyHandler
from idsw.etl.characterize import test_data_normality, partition_and_rank_df, histogram
from idsw.etl.meandifference import monte_carlo_simulation, generate_and_fit_distribution


class TestPlotlyIntegration(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)
        self.df = pd.DataFrame({
            'group': np.repeat(['A', 'B', 'C'], 25),
            'val': np.random.normal(50, 10, 75)
        })

    def test_plotly_handler_html_export(self):
        try:
            import plotly.graph_objects as go
        except ImportError:
            self.skipTest("plotly not installed")

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 5, 6])])
        with tempfile.TemporaryDirectory() as tmpdir:
            returned = PlotlyHandler.show_and_export(
                fig,
                export_file=True,
                directory_to_save=tmpdir,
                file_name="test_chart.png"
            )
            expected_html = os.path.join(tmpdir, "test_chart.html")
            self.assertTrue(os.path.exists(expected_html))
            self.assertEqual(returned, fig)

    def test_characterize_plotly_modes(self):
        try:
            import plotly
        except ImportError:
            self.skipTest("plotly not installed")

        with tempfile.TemporaryDirectory() as tmpdir:
            res = test_data_normality(
                self.df,
                column_to_analyze='val',
                export_png=True,
                directory_to_save=tmpdir,
                file_name='norm_prob',
                plotly=True
            )
            self.assertIsInstance(res, list)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "norm_prob.html")))

            ranked = partition_and_rank_df(
                self.df,
                column_for_partition='group',
                column_to_rank='val',
                export_png=True,
                directory_to_save=tmpdir,
                file_name='rank_box',
                plotly=True
            )
            self.assertIn('rank', ranked.columns)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "rank_box.html")))

            histogram(
                self.df,
                column_to_analyze='val',
                export_png=True,
                directory_to_save=tmpdir,
                file_name='hist_plot',
                plotly=True
            )
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "hist_plot.html")))

    def test_meandifference_plotly_modes(self):
        try:
            import plotly
        except ImportError:
            self.skipTest("plotly not installed")

        with tempfile.TemporaryDirectory() as tmpdir:
            sim_df, summ = monte_carlo_simulation(
                simulation_function_or_equation="x * 2 + y",
                input_distributions={'x': ('normal', 10, 2), 'y': ('uniform', 0, 5)},
                n_iterations=200,
                export_png=True,
                directory_to_save=tmpdir,
                file_name='mc_sim',
                plotly=True
            )
            self.assertEqual(len(sim_df), 200)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "mc_sim.html")))

            gen_df, fit_summ = generate_and_fit_distribution(
                distribution_name='normal',
                sample_size=200,
                export_png=True,
                directory_to_save=tmpdir,
                file_name='dist_fit',
                plotly=True
            )
            self.assertEqual(len(gen_df), 200)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "dist_fit.html")))


if __name__ == '__main__':
    unittest.main()
