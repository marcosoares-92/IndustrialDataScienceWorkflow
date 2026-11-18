"""
Interactive Plotly figure handler and utilities for IDSW v2.0.0.
Provides standardized handling for interactive Plotly figures,
HTML file export, and ControlVars display gating.
"""
import os

class PlotlyHandler:
    @staticmethod
    def show_and_export(fig, export_file=False, directory_to_save=None, file_name=None):
        """
        Gated presentation and HTML file export for Plotly figures.
        
        :param fig: plotly.graph_objects.Figure
        :param export_file: bool, whether to save as HTML
        :param directory_to_save: str, target directory
        :param file_name: str, file name (extension automatically converted to .html)
        :return: fig
        """
        from idsw import ControlVars

        if ControlVars.show_plots:
            try:
                fig.show()
            except Exception:
                pass

        if export_file and (file_name is not None or directory_to_save is not None):
            fname = file_name if file_name is not None else "idsw_plot.html"
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
                fname = os.path.splitext(fname)[0] + ".html"
            elif not fname.lower().endswith('.html'):
                fname = fname + ".html"
                
            target_path = os.path.join(directory_to_save, fname) if directory_to_save else fname
            try:
                fig.write_html(target_path)
                if ControlVars.show_results:
                    print(f"Interactive Plotly figure exported as HTML to: {target_path}")
            except Exception as e:
                if ControlVars.show_results:
                    print(f"Warning: Could not export Plotly HTML figure to {target_path}: {e}")
                    
        return fig
