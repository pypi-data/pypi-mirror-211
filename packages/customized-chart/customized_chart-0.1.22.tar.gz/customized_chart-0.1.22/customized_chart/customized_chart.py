import sys
from termcolor import colored
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np


#
# Sorts a dict by key or value.
#
def sort(data, field="value", reverse=False):
    idx = 1
    if field == "key":
        idx = 0
    data = dict(sorted(data.items(), key=lambda item: item[idx], reverse=reverse))
    return data


#
# Checks if a value is valid.
#
def valid(value, types, min_val=None, max_val=None, length=None):
    # Get caller function
    w = colored("Warning ", "red", attrs=["bold"]) + colored(f"{sys._getframe().f_back.f_code.co_name}", "blue") + ": " 

    if value is None:
        print(w + "value is none")
        return False
    if types is not None and type(value) not in types:
        print(w + f"value '{value}' is not a valid type (should be {','.join([x.__name__ for x in types])})")
        return False
    if type(value) == int and min_val is not None and value < min_val:
        print(w + f"value '{value}' is out of bounds (<{min_val})")
        return False
    if type(value) == int and max_val is not None and value > max_val:
        print(w + f"value '{value}' is out of bounds (>{max_val})")
        return False
    if type(value) == list and length is not None and len(value) != length:
        print(w + f"expected list size {length}, got {len(value)}")
        return False

    return True


#
# Parses a setting in options.
#
def parse_option(opts, param_name, default_val):
    if param_name not in opts:
        opts[param_name] = default_val


#
# Returns a scaled colormap (if found)
#
def fix_cmap(name, values):
    # Default
    if name is None:
        return None
    
    # Named colormap
    if type(name) == str:
        # Check if valid colormap, or use default
        cmaps = plt.colormaps()
        if name not in cmaps:
            print(colored("Warning: ", "red", attrs=["bold"]) + colored(str(name), "blue") + " is not a valid colormap, see")
            print("https://matplotlib.org/stable/gallery/color/colormap_reference.html")
            return None

        # Get colormap
        cmp = plt.get_cmap(name)

        # Get list of colors
        if hasattr(cmp, "colors"):
            cmp = cmp.colors
        else:
            cmp = cmp(np.arange(0,cmp.N))
    # Specified colors
    elif type(name) == list:
        cmp = []
        for c in name:
            c = c.lstrip("#")
            cmp.append(tuple(int(c[i:i+2], 16) / 255 for i in (0, 2, 4)))
        
    # Unknown type, return default
    else:
        return None
            
    # Multiply list if no values > no colors
    if len(values) > len(cmp):
        n = int(len(values)/len(cmp))+1
        cmp += cmp * n
        
    # Scale to number of values
    step = int(len(cmp) / len(values))
    step = min(int(len(cmp)/10), step)
    step = max(step, 1)
    
    colors = []
    for i in range(0,len(values)):
        colors.append(cmp[i*step])
    
    # Return scaled colormap
    return colors


#
# Formats a value to percent with specified number of decimals.
#
def percent_format(val, fmt):
    if fmt == "none":
        return ""
    if fmt == "pct-000":
        return f"{val*100:.0f}%"
    if fmt == "pct-1":
        return f"{val:.1f}%"
    if fmt == "pct-100":
        return f"{val*100:.1f}%"
    if fmt == "pct-2":
        return f"{val:.2f}%"
    if fmt == "pct-200":
        return f"{val*100:.2f}%"
    if fmt == "pct-3":
        return f"{val:.3f}%"
    if fmt == "pct-300":
        return f"{val*100:.3f}%"
    if fmt == "pct-4":
        return f"{val:.4f}%"
    if fmt == "pct-400":
        return f"{val*100:.4f}%"
    return f"{round(val):d}%"
    

#
# Formats a value with prefix (for example M for million).
#
def value_format(val, fmt):
    if type(fmt) != str:
        return val
    
    if fmt.startswith("prefix"):
        val = round(val)
        if type(val) not in [int,float]:
            return val

        prefixes = [
            [1e12, "T"],
            [1e9, "G"],
            [1e6, "M"],
            [1e3, "k"],
        ]

        # Iterate over prefixes
        for p in prefixes:
            if val >= p[0]:
                if val % p[0] == 0:
                    return f"{val/p[0]:.0f}{p[1]}"
                else:
                    if fmt.endswith("-2"):
                        return f"{val/p[0]:.2f}{p[1]}"
                    if fmt.endswith("-1"):
                        return f"{val/p[0]:.1f}{p[1]}"
                    if fmt.endswith("-0") or fmt == "prefix":
                        return f"{val/p[0]:.0f}{p[1]}"
                    return f"{val/p[0]}{p[1]}"

        # No prefix match
        return f"{val}"
    elif fmt.startswith("pct"):
        return percent_format(val, fmt)
    elif fmt.startswith("dec"):
        if fmt.endswith("-0"):
            return f"{round(val):d}"
        elif fmt.endswith("-1"):
            return f"{val:.1f}"
        elif fmt.endswith("-2"):
            return f"{val:.2f}"
        elif fmt.endswith("-3"):
            return f"{val:.3f}"
        elif fmt.endswith("-4"):
            return f"{val:.4f}"
        else:
            return f"{val}"
    elif fmt.startswith("int-"):
        if type(val) == int:
            return val
        if fmt.endswith("-0"):
            val = round(val)
            if type(val) == int or val.is_integer():
                return int(val)
            return f"{val:.0f}"
        if fmt.endswith("-1"):
            val = round(val,1)
            if type(val) == int or val.is_integer():
                return int(val)
            return f"{val:.1f}"
        elif fmt.endswith("-2"):
            val = round(val,2)
            if type(val) == int or val.is_integer():
                return int(val)
            return f"{val:.2f}"
        elif fmt.endswith("-3"):
            val = round(val,3)
            if type(val) == int or val.is_integer():
                return int(val)
            return f"{val:.3f}"
        elif fmt.endswith("-4"):
            val = round(val,4)
            if type(val) == int or val.is_integer():
                return int(val)
            return f"{val:.4f}"
        else:
            if type(val) == int or val.is_integer():
                return int(val)
            return f"{val}"
    elif fmt == "int":
        val = round(val)
        return int(val)
    else:
        return val


#
# Filter data to max n entries.
#
def filter_max_slices(data, n, other_label):
    # Sort data
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    # Create new data dict with other label
    ndata = {}
    other_val = 0
    for key,val in data.items():
        if len(ndata) >= n:
            other_val += val
        else:
            ndata.update({key: val})
    if other_val > 0:
        ndata.update({other_label: other_val})
    return ndata


#
# Generates a pie chart from a dict.
#
def pie_chart(data, opts=None):
    # Convert list/array to dict
    if type(data) in [list, np.ndarray]:
        tdata = {}
        for v in data:
            if v not in tdata:
                tdata.update({v: 0})
            tdata[v] += 1
        data = tdata
    # Check params  
    if not valid(data, [dict]): return
    if opts is None:
        opts = {}
    if not valid(opts, [dict]): return
    
    # Parse options
    parse_option(opts, "explode", None)
    parse_option(opts, "size", (12,8))
    parse_option(opts, "fontsize", 14)
    parse_option(opts, "title_fontsize", 18)
    parse_option(opts, "font", "Arial")
    parse_option(opts, "angle", 0)
    parse_option(opts, "show_total", False)
    parse_option(opts, "total", None)
    parse_option(opts, "show_missing", False)
    parse_option(opts, "missing_label", "-")
    parse_option(opts, "title", None)
    parse_option(opts, "show_counts", True)
    parse_option(opts, "other_label", "Other")
    parse_option(opts, "cmap", None)
    parse_option(opts, "shadow", False)
    parse_option(opts, "percent_format", "pct-1")
    parse_option(opts, "value_format", "")
    parse_option(opts, "label_color", "black")
    parse_option(opts, "label_distance", 0.6)
    parse_option(opts, "max_label_length", None)
    parse_option(opts, "max_label_sep", "...")
    parse_option(opts, "border", None)
    
    # Make a copy of the data (since it can be changed)
    data = data.copy()
    
    # Show max n slices (if set)
    if "max_slices" in opts and opts["max_slices"] is not None:
        data = filter_max_slices(data, opts["max_slices"], opts["other_label"])
    # Show missing
    if opts["show_missing"]:
        no_missing = opts["total"] - sum(data.values())
        if no_missing > 0:
            data.update({opts["missing_label"]: no_missing})
    
    # Plot settings
    plt.rcParams.update({"font.size": opts["fontsize"]})
    plt.rcParams.update({"font.family": opts["font"]})
    plt.figure(figsize=opts["size"])
    plt.axis("equal")
    plt.tight_layout()
    
    # Labels and values
    labels = data.keys()
    if opts["max_label_length"] is not None:
        nlabels = []
        for l in labels:
            if l != opts["other_label"] and l != opts["missing_label"]:
                nlabels.append(l[:opts["max_label_length"]] + opts["max_label_sep"])
            else:
                nlabels.append(l)
        labels = nlabels
    vals = data.values()
    
    # Set default cmap depending on no slices
    if opts["cmap"] is None:
        if len(labels) <= 20:
            opts["cmap"] = "tab20c"
        else:
            opts["cmap"] = "Spectral"
    
    # Slice label formatting
    def make_autopct(values):
        def m_autopct(pct):
            val = pct*sum(values)/100.0
            if opts["total"] is not None and type(opts["total"]) in [int,float]:
                pct = val / opts["total"] * 100
            l = percent_format(pct, opts["percent_format"])
            if opts["show_counts"]:
                l += f"  ({value_format(val, opts['value_format'])})"
            return l
        return m_autopct

    # Explode pie pieces
    if opts["explode"] is None:
        expl = [0] * len(data)
    else:
        expl = []
        for k in data.keys():
            if k in opts["explode"]:
                expl.append(0.1)
            else:
                expl.append(0)
    
    # Title
    if opts["title"] is not None:
        if opts["show_total"] and opts["title"] != "":
            if opts["total"] is not None and type(opts["total"]) in [int,float]:
                tot = opts["total"]
            else:
                tot = sum(vals)
            opts["title"] += f" ({value_format(tot, opts['value_format'])})"
        plt.title(opts["title"], fontweight="bold", fontsize=opts["title_fontsize"], y=1.04)
    
    # Border
    wp = None
    if opts["border"] is not None:
        wp = {"edgecolor": opts["border"][0], "linewidth": opts["border"][1]}
        
    # Generate pie
    plt.pie(vals, labels=labels, explode=expl, autopct=make_autopct(vals), pctdistance=opts["label_distance"], shadow=opts["shadow"], startangle=opts["angle"], colors=fix_cmap(opts["cmap"], vals), textprops={"color": opts["label_color"]}, wedgeprops=wp)
    
    plt.tight_layout()
    
    # Show it!
    plt.show()
    plt.close()


#
# Generates a bar chart from a dict.
#
def bar_chart(data, opts=None):
    # Convert list/array to dict
    if type(data) in [list, np.ndarray]:
        tdata = {}
        for v in data:
            if v not in tdata:
                tdata.update({v: 0})
            tdata[v] += 1
        data = tdata
    # Check params  
    if not valid(data, [dict]): return
    if opts is None:
        opts = {}
    if not valid(opts, [dict]): return
    
    # Parse options
    parse_option(opts, "size", (12,8))
    parse_option(opts, "fontsize", 14)
    parse_option(opts, "title_fontsize", 18)
    parse_option(opts, "font", "Arial")
    parse_option(opts, "show_total", False)
    parse_option(opts, "title", None)
    parse_option(opts, "other_label", "Other")
    parse_option(opts, "color", "#3976ae")
    parse_option(opts, "value_format", "")
    parse_option(opts, "label_rotation", 0)
    parse_option(opts, "bar_label", False)
    parse_option(opts, "bar_label_color", "#666")
    parse_option(opts, "y_label", None)
    parse_option(opts, "y_label_color", "#244a6e")
    parse_option(opts, "x_label", None)
    parse_option(opts, "x_label_color", "#244a6e")
    parse_option(opts, "horizontal", False)
    parse_option(opts, "grid", False)
    parse_option(opts, "y_lim", None)
    
    # Show max n slices (if set)
    if "max_slices" in opts and opts["max_slices"] is not None:
        data = filter_max_slices(data, opts["max_slices"], opts["other_label"])
    
    # Plot settings
    plt.rcParams.update({"font.size": opts["fontsize"]})
    plt.rcParams.update({"font.family": opts["font"]})
    plt.figure(figsize=opts["size"])
    plt.tight_layout()
    
    # Labels and values
    labels = data.keys()
    vals = data.values()
    plt.xticks(rotation=opts["label_rotation"])
    
    # Title
    if opts["title"] is not None:
        if opts["show_total"] and opts["title"] != "":
            opts["title"] += f" ({sum(vals)})"
        plt.title(opts["title"], fontweight="bold", fontsize=opts["title_fontsize"], y=1.04)
    
    # Generate bar
    if opts["horizontal"]:
        bars = plt.barh(list(labels), list(vals), color=opts["color"])
        if opts["grid"]:
            plt.grid(axis="x", color ="grey", linewidth=0.5, alpha=0.2)
    else:
        bars = plt.bar(labels, vals, color=opts["color"])
        if opts["grid"]:
            plt.grid(axis="y", color ="grey", linewidth=0.5, alpha=0.2)
    
    # Bar labels
    if opts["bar_label"]:
        plt.bar_label(bars, labels=[value_format(x,opts["value_format"]) for x in vals], color=opts["bar_label_color"], padding=1)
    
    # Axis labels
    if opts["y_label"] is not None:
        plt.ylabel(opts["y_label"], color=opts["y_label_color"], fontweight="bold")
    if opts["x_label"] is not None:
        plt.xlabel(opts["x_label"], color=opts["x_label_color"], fontweight="bold")
    
    # Set y-label format to prefix
    if opts["value_format"].startswith("prefix"):
        def label_formatter(x, pos):
            return value_format(int(x), opts["value_format"])
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(label_formatter))
    
    if opts["y_lim"] is not None:
        plt.ylim(opts["y_lim"])
        
    # Show it!
    plt.show()
    plt.close()
    
    
#
# Generates a grouped bar chart from a dict.
#
def grouped_bar_chart(data, opts=None):
    # Check params  
    if not valid(data, [dict]): return
    if opts is None:
        opts = {}
    if not valid(opts, [dict]): return
    
    # Parse options
    parse_option(opts, "size", (14,6))
    parse_option(opts, "fontsize", 14)
    parse_option(opts, "title_fontsize", 18)
    parse_option(opts, "font", "Arial")
    parse_option(opts, "title", None)
    parse_option(opts, "cmap", "Paired")
    parse_option(opts, "colors", None)
    parse_option(opts, "value_format", "")
    parse_option(opts, "label_rotation", 0)
    parse_option(opts, "bar_labels", False)
    parse_option(opts, "bar_width", 0.8 / len(data["series"]))
    parse_option(opts, "y_label", None)
    parse_option(opts, "y_label_color", "#244a6e")
    parse_option(opts, "x_label", None)
    parse_option(opts, "x_label_color", "#244a6e")
    parse_option(opts, "grid", False)
    parse_option(opts, "y_lim", None)
    parse_option(opts, "legend", True)
    parse_option(opts, "legend_position", None)
    parse_option(opts, "bbox", None)
    
    # Plot settings
    plt.rcParams.update({"font.size": opts["fontsize"]})
    plt.rcParams.update({"font.family": opts["font"]})
    plt.figure(figsize=opts["size"])
    plt.tight_layout()
    plt.xticks(rotation=opts["label_rotation"])
    
    # Title
    if opts["title"] is not None:
        plt.title(opts["title"], fontweight="bold", fontsize=opts["title_fontsize"], y=1.04)
    
    # Labels and bars
    data["n"] = len(data["series"])
    x = np.arange(len(data["labels"])) # label locations
    width = opts["bar_width"] # bar width
    spacing = width + 0.02 # spacing
    spos = -spacing * data["n"]/2 + spacing/2
    ax = plt.gca()
    
    # Colors
    if opts["colors"] is None:
        cols = fix_cmap(opts["cmap"], data["series"])
    else:
        cols = opts["colors"]
        if data["n"] > len(cols):
            n = int(data["n"]/len(cols))+1
            cols += cols * n
        
    # Generate bars
    bars = []
    for i in range(0,data["n"]):
        bars.append(ax.bar(x + spacing*i + spos, data["values"][i], width, label=data["series"][i], color=cols[i]))
    
    # X-ticks
    ax.set_xticks(x)
    ax.set_xticklabels(data["labels"])
    
    # Legend
    if opts["legend"]:
        if opts["legend_position"] is None:
            ax.legend()
        else:
            if opts["bbox"] is None:
                ax.legend(loc=opts["legend_position"])
            else:
                ax.legend(loc=opts["legend_position"], bbox_to_anchor=opts["bbox"])
                
    # Bar labels
    if opts["bar_labels"]:
        for i in range(0,data["n"]):
            ax.bar_label(bars[i], labels=[value_format(x,opts["value_format"]) for x in data["values"][i]], padding=1)
    
    # Grid
    if opts["grid"]:
        plt.grid(axis="y", color ="grey", linewidth=0.5, alpha=0.2)
    
    # Axis labels
    if opts["y_label"] is not None:
        plt.ylabel(opts["y_label"], color=opts["y_label_color"], fontweight="bold")
    if opts["x_label"] is not None:
        plt.xlabel(opts["x_label"], color=opts["x_label_color"], fontweight="bold")
    
    # Set y-label format to prefix
    if opts["value_format"].startswith("prefix"):
        def label_formatter(x, pos):
            return value_format(int(x), opts["value_format"])
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(label_formatter))
    
    if opts["y_lim"] is not None:
        plt.ylim(opts["y_lim"])
        
    # Show it!
    plt.show()
    plt.close()


#
# Generates a series of labels (integers, months, quarters).
#
def generate_labels(fmt, n):
    if fmt.startswith("range"):
        sv = 0
        if " " in fmt:
            sv = int(fmt.split(" ")[1])
        return list(range(sv,n+sv))
    if fmt.startswith("month"):
        sy = 2020
        if " " in fmt:
            sy = int(fmt.split(" ")[1])
        m = 1
        labels = []
        for i in range(0,n):
            labels.append(f"{sy}-{str(m).zfill(2)}")
            m += 1
            if m > 12:
                m = 1
                sy += 1
        return labels
    if fmt.startswith("quarter"):
        sy = 2020
        if " " in fmt:
            sy = int(fmt.split(" ")[1])
        m = 1
        labels = []
        for i in range(0,n):
            labels.append(f"{sy}-Q{m}")
            m += 1
            if m > 4:
                m = 1
                sy += 1
        return labels


#
# Generates a line chart from a dict or list.
#
def line_chart(data, opts=None):
    # Check params  
    if not valid(data, [dict, list, np.ndarray]): return
    if opts is None:
        opts = {}
    if not valid(opts, [dict]): return
    
    # Parse options
    parse_option(opts, "size", (14,6))
    parse_option(opts, "fontsize", 14)
    parse_option(opts, "title_fontsize", 18)
    parse_option(opts, "font", "Arial")
    parse_option(opts, "title", None)
    parse_option(opts, "color", "#3976ae")
    parse_option(opts, "value_format", "")
    parse_option(opts, "label_rotation", 0)
    parse_option(opts, "y_label", None)
    parse_option(opts, "y_label_color", "#244a6e")
    parse_option(opts, "y_lim", None)
    parse_option(opts, "x_label", None)
    parse_option(opts, "x_label_color", "#244a6e")
    parse_option(opts, "grid", False)
    parse_option(opts, "labels", "range 0")
    parse_option(opts, "labels_fontsize", 12)
    parse_option(opts, "trend", False)
    parse_option(opts, "trend_color", "#e80613")
    parse_option(opts, "show_values", False)
    parse_option(opts, "show_values_step", 1)
    
    # Convert values
    if type(data) == dict:
        vals = list(data.values())
        labels = list(data.keys())
    else:
        vals = data
        labels = generate_labels(opts["labels"], len(vals))
        
    # Plot settings
    plt.rcParams.update({"font.size": opts["fontsize"]})
    plt.rcParams.update({"font.family": opts["font"]})
    plt.figure(figsize=opts["size"])
    plt.tight_layout()
    
    plt.xticks(fontsize=opts["labels_fontsize"], rotation=opts["label_rotation"])
    
    # Title
    if opts["title"] is not None:
        plt.title(opts["title"], fontweight="bold", fontsize=opts["title_fontsize"], y=1.04)
    
    # Generate line
    if labels is not None:
        plt.plot(labels, vals, color=opts["color"], linewidth=2)   
    else:
        plt.plot(vals, color=opts["color"], linewidth=2)
        
    # Show values
    if opts["show_values"]:
        i = 0
        for x, y in zip(labels, vals):
            if i % opts["show_values_step"] == 0:
                plt.annotate(value_format(y, opts["value_format"]), (x,y), xycoords="data", textcoords="offset points", xytext=(0,10), ha="center")
            i += 1
        
    # Grid
    if opts["grid"]:
        plt.grid(axis="y", color ="grey", linewidth=0.5, alpha=0.2)
    
    # Trend line
    if opts["trend"]:
        p = np.poly1d(np.polyfit(range(0,len(vals)), vals, 1))
        trend = [p(x) for x in range(0,len(vals))]
        plt.plot(trend, color=opts["trend_color"], linestyle="--", linewidth=1)
    
    # Axis labels
    if opts["y_label"] is not None:
        plt.ylabel(opts["y_label"], color=opts["y_label_color"], fontweight="bold")
    if opts["x_label"] is not None:
        plt.xlabel(opts["x_label"], color=opts["x_label_color"], fontweight="bold")
    
    # Set y-label format
    if opts["value_format"] != "":
        def label_formatter(x, pos):
            return value_format(x, opts["value_format"])
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(label_formatter))
    
    if opts["y_lim"] is not None:
        plt.ylim(opts["y_lim"])
    
    # Show it!
    plt.show()
    plt.close()
    

#
# Generates multiple line charts a list of dicts or lists.
#
def multi_line_chart(data, opts=None):
    # Check params  
    if not valid(data, [dict]): return
    if opts is None:
        opts = {}
    if not valid(opts, [dict]): return
    
    # Parse options
    parse_option(opts, "size", (14,6))
    parse_option(opts, "fontsize", 14)
    parse_option(opts, "title_fontsize", 18)
    parse_option(opts, "font", "Arial")
    parse_option(opts, "title", None)
    parse_option(opts, "value_format", "")
    parse_option(opts, "label_rotation", 0)
    parse_option(opts, "y_label", None)
    parse_option(opts, "y_label_color", "#244a6e")
    parse_option(opts, "y_lim", None)
    parse_option(opts, "x_label", None)
    parse_option(opts, "x_label_color", "#244a6e")
    parse_option(opts, "grid", False)
    parse_option(opts, "labels", "range 0")
    parse_option(opts, "labels_fontsize", 12)
    parse_option(opts, "trend", False)
    parse_option(opts, "show_values", False)
    parse_option(opts, "show_values_step", 1)
    parse_option(opts, "cmap", "Paired")
    parse_option(opts, "legend", True)
    parse_option(opts, "legend_position", None)
    parse_option(opts, "bbox", None)
    
    # Plot settings
    plt.rcParams.update({"font.size": opts["fontsize"]})
    plt.rcParams.update({"font.family": opts["font"]})
    plt.figure(figsize=opts["size"])
    plt.tight_layout()
    
    plt.xticks(fontsize=opts["labels_fontsize"], rotation=opts["label_rotation"])
    
    # Title
    if opts["title"] is not None:
        plt.title(opts["title"], fontweight="bold", fontsize=opts["title_fontsize"], y=1.04)
    
    # Convert values
    colors=fix_cmap(opts["cmap"], range(0,len(data["values"])))
    for vals,col in zip(data["values"],colors):
        if "labels" in data and data["labels"] is not None:
            labels = data["labels"]
            if not valid(labels, [list], length=len(vals)):
                return
        else:
            labels = generate_labels(opts["labels"], len(vals))

        # Generate line
        if labels is not None:
            plt.plot(labels, vals, color=col, linewidth=2)
        else:
            plt.plot(vals, color=col, linewidth=2)
            
        # Show values
        if opts["show_values"]:
            i = 0
            for x, y in zip(labels, vals):
                if i % opts["show_values_step"] == 0:
                    plt.annotate(value_format(y, opts["value_format"]), (x,y), xycoords="data", textcoords="offset points", xytext=(0,10), ha="center")
                i += 1
    
    # Legend
    if opts["legend"]:
        if opts["legend_position"] is None:
            plt.gca().legend(data["series"])
        else:
            if opts["bbox"] is None:
                plt.gca().legend(data["series"], loc=opts["legend_position"])
            else:
                plt.gca().legend(data["series"], loc=opts["legend_position"], bbox_to_anchor=opts["bbox"])

    # Trend lines
    if opts["trend"]:
        for e,col in zip(data["values"],colors):
            if type(e) == dict:
                vals = list(e.values())
            else:
                vals = e
            p = np.poly1d(np.polyfit(range(0,len(vals)), vals, 1))
            trend = [p(x) for x in range(0,len(vals))]
            plt.plot(trend, color=col, linestyle="--", linewidth=1)
    
    # Grid
    if opts["grid"]:
        plt.grid(axis="y", color ="grey", linewidth=0.5, alpha=0.2)
    
    # Axis labels
    if opts["y_label"] is not None:
        plt.ylabel(opts["y_label"], color=opts["y_label_color"], fontweight="bold")
    if opts["x_label"] is not None:
        plt.xlabel(opts["x_label"], color=opts["x_label_color"], fontweight="bold")
    
    # Set y-label format
    if opts["value_format"] != "":
        def label_formatter(x, pos):
            return value_format(x, opts["value_format"])
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(label_formatter))
    
    if opts["y_lim"] is not None:
        plt.ylim(opts["y_lim"])
    
    # Show it!
    plt.show()
    plt.close()


#
# Generate boxplots.
#
def box_plot(data, opts={}):
    # Check params  
    if not valid(data, [dict,list]): return
    if opts is None:
        opts = {}
    if not valid(opts, [dict]): return
    
    # Convert data to dict (if needed)
    if type(data) == list:
        data = {
            "values": data,
        }

    # Parse options
    parse_option(opts, "size", (14,6))
    parse_option(opts, "fontsize", 14)
    parse_option(opts, "title_fontsize", 18)
    parse_option(opts, "font", "Arial")
    parse_option(opts, "title", None)
    parse_option(opts, "value_format", "")
    parse_option(opts, "label_rotation", 0)
    parse_option(opts, "y_label", None)
    parse_option(opts, "y_label_color", "#244a6e")
    parse_option(opts, "lim", None)
    parse_option(opts, "x_label", None)
    parse_option(opts, "x_label_color", "#244a6e")
    parse_option(opts, "grid", False)
    parse_option(opts, "labels", "range 0")
    parse_option(opts, "labels_fontsize", 12)
    parse_option(opts, "labels_color", "#000")
    parse_option(opts, "cmap", "Paired")
    parse_option(opts, "horizontal", False)
    
    # Plot settings
    plt.rcParams.update({"font.size": opts["fontsize"]})
    plt.rcParams.update({"font.family": opts["font"]})
    plt.figure(figsize=opts["size"])
    plt.tight_layout()
    
    if opts["horizontal"]:
        plt.yticks(fontsize=opts["labels_fontsize"], rotation=opts["label_rotation"], color=opts["labels_color"])
    else:
        plt.xticks(fontsize=opts["labels_fontsize"], rotation=opts["label_rotation"], color=opts["labels_color"])
    
    # Title
    if opts["title"] is not None:
        plt.title(opts["title"], fontweight="bold", fontsize=opts["title_fontsize"], y=1.04)
    
    # Grid
    if opts["grid"]:
        plt.grid(axis="y", color ="grey", linewidth=0.5, alpha=0.2)
        
    # Labels
    if "series" in data and data["series"] is not None:
        labels = data["series"]
        if not valid(labels, [list], length=len(data["series"])):
            return
    else:
        labels = generate_labels(opts["labels"], len(data["values"]))
    
    # Axis labels
    if opts["y_label"] is not None:
        plt.ylabel(opts["y_label"], color=opts["y_label_color"], fontweight="bold")
    if opts["x_label"] is not None:
        plt.xlabel(opts["x_label"], color=opts["x_label_color"], fontweight="bold")
    
    # Set y-label format
    if opts["value_format"] != "":
        def label_formatter(x, pos):
            return value_format(x, opts["value_format"])
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(label_formatter))
    
    if opts["lim"] is not None:
        if opts["horizontal"]:
            plt.xlim(opts["lim"])
        else:
            plt.ylim(opts["lim"])
    
    # Create plot
    if opts["horizontal"]:
        vert = False
    else:
        vert = True
    bp = plt.boxplot(data["values"], labels=labels, patch_artist=True, vert=vert)
    
    # Colors
    colors=fix_cmap(opts["cmap"], range(0,len(data["values"])))
    for i,patch in enumerate(bp["boxes"]):
        patch.set(facecolor=colors[i]) 
    
    # Show it!
    plt.show()
    plt.close()
