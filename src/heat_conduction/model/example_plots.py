from typing import Dict, List, Any, Optional, Union
import numpy as np
import math

def generate_line_plot() -> Dict:
    id = "1"
    title = "Line Plot"
    x_values = list(np.linspace(0, 10, 100))
    y_values = [np.sin(x) for x in x_values]
    trace_name = "Line Trace"
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    y_axis_range = None
    line_color = "rgb(0,83,138)"
    line_dash = "0"
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "name": trace_name,
                "type": "scattergl",
                "showlegend": True,
                "visible": True,
                "text": "",
                "textposition": "",
                "x": x_values,
                "y": y_values,
                "line": {
                    "color": line_color,
                    "dash": line_dash
                },
                "mode": "lines"
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "annotations": [],
            "margin": {},
            "legend": {
                "x": 0.98,
                "xanchor": "right",
                "y": 0.98,
                "yanchor": "top",
                "borderwidth": 1,
                "bgcolor": "rgba(180,180,180,0.2)"
            }
        }
    }
    
    if y_axis_range:
        plot_config["layout"]["yaxis"]["range"] = y_axis_range
    
    return plot_config


def generate_multi_line_plot() -> Dict:
    id = "2"
    title = "Multiple Lines Plot"
    x = list(np.linspace(0, 2*np.pi, 100))
    traces = [
        {"x": x, "y": [np.sin(v) for v in x], "name": "sin(x)", "color": "rgb(0,83,138)"},
        {"x": x, "y": [np.cos(v) for v in x], "name": "cos(x)", "color": "rgb(212,73,30)"}
    ]
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    y_axis_range = None
    
    plot_data = []
    colors = ["rgb(0,83,138)", "rgb(212,73,30)", "rgb(17,119,51)", 
              "rgb(153,70,193)", "rgb(230,122,36)"]
    
    for i, trace in enumerate(traces):
        trace_data = {
            "name": trace.get("name", f"Trace {i+1}"),
            "type": "scattergl",
            "showlegend": True,
            "visible": True,
            "x": trace.get("x", []),
            "y": trace.get("y", []),
            "line": {
                "color": trace.get("color", colors[i % len(colors)]),
                "dash": trace.get("dash", "0")
            },
            "mode": trace.get("mode", "lines")
        }
        plot_data.append(trace_data)
    
    plot_config = {
        "id": id,
        "title": title,
        "data": plot_data,
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "annotations": [],
            "margin": {},
            "legend": {
                "x": 0.98,
                "xanchor": "right",
                "y": 0.98,
                "yanchor": "top",
                "borderwidth": 1,
                "bgcolor": "rgba(180,180,180,0.2)"
            }
        }
    }
    
    if y_axis_range:
        plot_config["layout"]["yaxis"]["range"] = y_axis_range
    
    return plot_config


def generate_scatter_plot() -> Dict:
    id = "3"
    title = "Scatter Plot"
    np.random.seed(42)
    x_values = np.random.normal(0, 1, 50).tolist()
    y_values = np.random.normal(0, 1, 50).tolist()
    trace_name = "Data Points"
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    marker_color = "rgb(0,83,138)"
    marker_size = 8
    marker_symbol = "circle"
    opacity = 0.8
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "name": trace_name,
                "type": "scattergl",
                "showlegend": True,
                "visible": True,
                "x": x_values,
                "y": y_values,
                "marker": {
                    "color": marker_color,
                    "size": marker_size,
                    "symbol": marker_symbol,
                    "opacity": opacity
                },
                "mode": "markers"
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "annotations": [],
            "margin": {},
            "legend": {
                "x": 0.98,
                "xanchor": "right",
                "y": 0.98,
                "yanchor": "top",
                "borderwidth": 1,
                "bgcolor": "rgba(180,180,180,0.2)"
            }
        }
    }
    
    return plot_config


def generate_bar_plot() -> Dict:
    id = "4"
    title = "Bar Chart"
    x_categories = ["Category A", "Category B", "Category C", "Category D", "Category E"]
    y_values = [23, 17, 35, 29, 12]
    trace_name = "Bar Values"
    x_axis_title = "Categories"
    y_axis_title = "Values"
    bar_color = "rgb(0,83,138)"
    orientation = "v" 
    
    trace = {
        "name": trace_name,
        "type": "bar",
        "showlegend": True,
        "visible": True,
        "marker": {
            "color": bar_color
        }
    }
    
    if orientation == 'v':
        trace["x"] = x_categories
        trace["y"] = y_values
    else:
        trace["y"] = x_categories
        trace["x"] = y_values
        trace["orientation"] = "h"
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [trace],
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "annotations": [],
            "margin": {},
            "legend": {
                "x": 0.98,
                "xanchor": "right",
                "y": 0.98,
                "yanchor": "top",
                "borderwidth": 1,
                "bgcolor": "rgba(180,180,180,0.2)"
            }
        }
    }
    
    return plot_config


def generate_heatmap() -> Dict:
    id = "5"
    title = "Heatmap"
    x = np.linspace(-5, 5, 30)
    y = np.linspace(-5, 5, 30)
    z_data = []
    for yi in y:
        row = []
        for xi in x:
            distance = math.sqrt(xi**2 + yi**2)
            if distance == 0:
                row.append(1.0)
            else:
                row.append(math.sin(distance) / distance)
        z_data.append(row)
    
    x_labels = [f"{v:.1f}" for v in x]
    y_labels = [f"{v:.1f}" for v in y]
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    colorscale = "Viridis"
    show_scale = True
    z_min = None
    z_max = None
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "type": "heatmap",
                "z": z_data,
                "x": x_labels,
                "y": y_labels,
                "colorscale": colorscale,
                "showscale": show_scale,
                "name": "Heatmap Data"
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "annotations": [],
            "margin": {}
        }
    }
    
    if z_min is not None:
        plot_config["data"][0]["zmin"] = z_min
    if z_max is not None:
        plot_config["data"][0]["zmax"] = z_max
    
    return plot_config


def generate_3d_scatter() -> Dict:
    id = "6"
    title = "3D Scatter Plot"
    t = np.linspace(0, 10*np.pi, 100)
    x_values = (np.sin(t) * t/10).tolist()
    y_values = (np.cos(t) * t/10).tolist()
    z_values = t.tolist()
    trace_name = "3D Data Points"
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    z_axis_title = "Z Axis"
    marker_color = "rgb(0,83,138)"
    marker_size = 5
    marker_opacity = 0.8
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "name": trace_name,
                "type": "scatter3d",
                "showlegend": True,
                "visible": True,
                "x": x_values,
                "y": y_values,
                "z": z_values,
                "marker": {
                    "color": marker_color,
                    "size": marker_size,
                    "opacity": marker_opacity
                },
                "mode": "markers"
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "scene": {
                "xaxis": {"title": x_axis_title},
                "yaxis": {"title": y_axis_title},
                "zaxis": {"title": z_axis_title},
                "camera": {
                    "eye": {"x": 1.5, "y": 1.5, "z": 1.5}
                }
            },
            "margin": {"l": 0, "r": 0, "t": 50, "b": 0},
            "legend": {
                "x": 0.98,
                "xanchor": "right",
                "y": 0.98,
                "yanchor": "top",
                "borderwidth": 1,
                "bgcolor": "rgba(180,180,180,0.2)"
            }
        }
    }
    
    return plot_config


def generate_3d_surface() -> Dict:
    id = "7"
    title = "3D Surface Plot"
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    z_data = []
    for yi in y:
        row = []
        for xi in x:
            r = math.sqrt(xi**2 + yi**2)
            if r == 0:
                row.append(1.0)
            else:
                row.append(math.sin(r) / r)
        z_data.append(row)
    
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    z_axis_title = "Z Axis"
    colorscale = "Viridis"
    show_scale = True
    opacity = 1.0
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "type": "surface",
                "z": z_data,
                "colorscale": colorscale,
                "showscale": show_scale,
                "opacity": opacity,
                "name": "Surface Plot"  # Add this line to fix the validation error
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "scene": {
                "xaxis": {"title": x_axis_title},
                "yaxis": {"title": y_axis_title},
                "zaxis": {"title": z_axis_title},
                "camera": {
                    "eye": {"x": 1.5, "y": 1.5, "z": 1.5}
                }
            },
            "margin": {"l": 0, "r": 0, "t": 50, "b": 0}
        }
    }
    
    return plot_config


def generate_contour_plot() -> Dict:
    id = "8"
    title = "Contour Plot"
    x = np.linspace(-3, 3, 40)
    y = np.linspace(-3, 3, 40)
    z_data = []
    for yi in y:
        row = []
        for xi in x:
            r = xi**2 + yi**2
            row.append(math.exp(-r/2))
        z_data.append(row)
    
    x_values = x.tolist()
    y_values = y.tolist()
    x_axis_title = "X Axis"
    y_axis_title = "Y Axis"
    colorscale = "Viridis"
    contours_coloring = "heatmap"
    show_scale = True
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "type": "contour",
                "z": z_data,
                "x": x_values,
                "y": y_values,
                "colorscale": colorscale,
                "contours": {
                    "coloring": contours_coloring
                },
                "showscale": show_scale,
                "name": "Contour Data" 
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "margin": {}
        }
    }
    
    return plot_config


def generate_histogram() -> Dict:
    id = "9"
    title = "Histogram"
    np.random.seed(42)
    x_values = np.random.normal(0, 1, 1000).tolist()
    trace_name = "Distribution"
    x_axis_title = "Values"
    y_axis_title = "Count"
    marker_color = "rgb(0,83,138)"
    nbins = 30
    opacity = 0.7
    
    plot_config = {
        "id": id,
        "title": title,
        "data": [
            {
                "name": trace_name,
                "type": "histogram",
                "showlegend": True,
                "visible": True,
                "x": x_values,
                "marker": {
                    "color": marker_color,
                    "opacity": opacity
                },
                "nbinsx": nbins
            }
        ],
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "bargap": 0.1,
            "margin": {},
            "legend": {
                "x": 0.98,
                "xanchor": "right",
                "y": 0.98,
                "yanchor": "top",
                "borderwidth": 1,
                "bgcolor": "rgba(180,180,180,0.2)"
            }
        }
    }
    
    return plot_config


def generate_box_plot() -> Dict:
    id = "10"
    title = "Box Plot"
    np.random.seed(42)
    data_groups = [
        {"y": np.random.normal(0, 1, 50).tolist(), "name": "Group A"},
        {"y": np.random.normal(2, 0.8, 50).tolist(), "name": "Group B"},
        {"y": np.random.normal(1, 1.2, 50).tolist(), "name": "Group C"},
        {"y": np.random.normal(3, 1.5, 50).tolist(), "name": "Group D"}
    ]
    x_axis_title = "Groups"
    y_axis_title = "Values"
    box_colors = ["rgb(0,83,138)", "rgb(212,73,30)", 
                 "rgb(17,119,51)", "rgb(153,70,193)"]
    
    traces = []
    for i, group in enumerate(data_groups):
        color = box_colors[i % len(box_colors)]
        trace = {
            "type": "box",
            "y": group["y"],
            "name": group.get("name", f"Group {i+1}"),
            "marker": {"color": color},
            "showlegend": False
        }
        if "x" in group:
            trace["x"] = group["x"]
        traces.append(trace)
    
    plot_config = {
        "id": id,
        "title": title,
        "data": traces,
        "layout": {
            "title": {
                "text": title
            },
            "xaxis": {
                "title": x_axis_title
            },
            "yaxis": {
                "title": y_axis_title
            },
            "margin": {}
        }
    }
    
    return plot_config