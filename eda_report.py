import csv
import os
from collections import Counter, defaultdict
from math import ceil

DATA_FILE = 'debtdata.csv'
OUT_DIR = 'analysis'
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- Utility functions ----------
def read_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_svg(path, width, height, content):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.title {{ font: bold 20px sans-serif; fill: #1f2937; }}
.label {{ font: 12px sans-serif; fill: #374151; }}
.small {{ font: 11px sans-serif; fill: #6b7280; }}
.axis {{ stroke: #9ca3af; stroke-width: 1; }}
.grid {{ stroke: #e5e7eb; stroke-width: 1; }}
</style>
{content}
</svg>'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)


def bar_chart_horizontal(title, subtitle, labels, values, out_path, color='#2563eb'):
    width, height = 1100, 650
    margin_left, margin_right, margin_top, margin_bottom = 280, 50, 90, 50
    chart_w = width - margin_left - margin_right
    row_h = (height - margin_top - margin_bottom) / max(1, len(labels))
    vmax = max(values) if values else 1

    parts = [
        f'<text x="30" y="35" class="title">{title}</text>',
        f'<text x="30" y="58" class="small">{subtitle}</text>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" class="axis" />'
    ]

    for i, (lbl, v) in enumerate(zip(labels, values)):
        y = margin_top + i * row_h + row_h * 0.18
        bar_h = row_h * 0.64
        bar_w = (v / vmax) * chart_w
        parts.append(f'<rect x="{margin_left}" y="{y}" width="{bar_w:.2f}" height="{bar_h:.2f}" fill="{color}" rx="3" />')
        parts.append(f'<text x="{margin_left-10}" y="{y + bar_h*0.7:.2f}" text-anchor="end" class="label">{lbl}</text>')
        parts.append(f'<text x="{margin_left + bar_w + 8:.2f}" y="{y + bar_h*0.7:.2f}" class="label">{v}</text>')

    for tick in range(0, 6):
        val = int(vmax * tick / 5)
        x = margin_left + chart_w * tick / 5
        parts.append(f'<line x1="{x:.2f}" y1="{margin_top}" x2="{x:.2f}" y2="{height-margin_bottom}" class="grid" />')
        parts.append(f'<text x="{x:.2f}" y="{height-20}" text-anchor="middle" class="small">{val}</text>')

    write_svg(out_path, width, height, '\n'.join(parts))


def line_chart(title, subtitle, x_labels, y_values, out_path, color='#059669'):
    width, height = 1200, 620
    ml, mr, mt, mb = 70, 30, 80, 60
    cw, ch = width - ml - mr, height - mt - mb
    n = len(x_labels)
    vmax = max(y_values) if y_values else 1
    vmin = min(y_values) if y_values else 0
    if vmax == vmin:
        vmax += 1

    points = []
    for i, yv in enumerate(y_values):
        x = ml + (i / (n-1 if n > 1 else 1)) * cw
        y = mt + (1 - ((yv - vmin) / (vmax - vmin))) * ch
        points.append((x, y, yv))

    parts = [
        f'<text x="30" y="35" class="title">{title}</text>',
        f'<text x="30" y="58" class="small">{subtitle}</text>',
        f'<line x1="{ml}" y1="{mt+ch}" x2="{ml+cw}" y2="{mt+ch}" class="axis" />',
        f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ch}" class="axis" />'
    ]

    for tick in range(0, 6):
        val = vmin + (vmax-vmin) * tick / 5
        y = mt + (1 - tick/5) * ch
        parts.append(f'<line x1="{ml}" y1="{y:.2f}" x2="{ml+cw}" y2="{y:.2f}" class="grid" />')
        parts.append(f'<text x="{ml-10}" y="{y+4:.2f}" text-anchor="end" class="small">{int(round(val))}</text>')

    polyline = ' '.join(f'{x:.2f},{y:.2f}' for x, y, _ in points)
    parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{polyline}" />')

    step = max(1, n // 12)
    for i, (x, y, yv) in enumerate(points):
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="{color}" />')
        if i % step == 0 or i == n-1:
            parts.append(f'<text x="{x:.2f}" y="{mt+ch+20}" text-anchor="middle" class="small">{x_labels[i]}</text>')

    write_svg(out_path, width, height, '\n'.join(parts))


def heatmap(title, subtitle, rows, cols, matrix, out_path):
    width, height = 1200, 700
    ml, mr, mt, mb = 230, 50, 100, 80
    cw, ch = width - ml - mr, height - mt - mb
    cell_w = cw / max(1, len(cols))
    cell_h = ch / max(1, len(rows))
    vmax = max(max(r) if r else 0 for r in matrix) or 1

    def color(v):
        t = v / vmax
        r = int(239 - t * 190)
        g = int(246 - t * 120)
        b = int(255 - t * 180)
        return f'rgb({r},{g},{b})'

    parts = [
        f'<text x="30" y="35" class="title">{title}</text>',
        f'<text x="30" y="58" class="small">{subtitle}</text>'
    ]

    for i, rname in enumerate(rows):
        y = mt + i * cell_h
        parts.append(f'<text x="{ml-10}" y="{y + cell_h*0.65:.2f}" text-anchor="end" class="small">{rname}</text>')
        for j, cname in enumerate(cols):
            x = ml + j * cell_w
            v = matrix[i][j]
            parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_w:.2f}" height="{cell_h:.2f}" fill="{color(v)}" stroke="#e5e7eb" />')
            if v > 0:
                parts.append(f'<text x="{x+cell_w/2:.2f}" y="{y+cell_h*0.6:.2f}" text-anchor="middle" class="small">{v}</text>')

    for j, cname in enumerate(cols):
        x = ml + j * cell_w + cell_w / 2
        parts.append(f'<text x="{x:.2f}" y="{mt-12}" text-anchor="middle" class="small">{cname}</text>')

    write_svg(out_path, width, height, '\n'.join(parts))

# ---------- Analysis ----------
rows = read_rows(DATA_FILE)

country_counts = Counter(r['country'] for r in rows)
year_counts = Counter(int(r['year']) for r in rows)
currency_counts = Counter(r['debt_amount'] for r in rows)
type_counts = Counter(r['debt_type'] for r in rows)
reason_counts = Counter(r['debt_reason'] for r in rows)
status_counts = Counter(r['debt_status'] for r in rows)

# Rankings
country_top15 = country_counts.most_common(15)
currency_top12 = currency_counts.most_common(12)

years = sorted(year_counts)
yvals = [year_counts[y] for y in years]

# Debt burden groupings by quartile over country record counts
all_counts = sorted(country_counts.values())
q1 = all_counts[len(all_counts)//4]
q2 = all_counts[len(all_counts)//2]
q3 = all_counts[(3*len(all_counts))//4]

groups = {'Low':0, 'Moderate':0, 'High':0, 'Very High':0}
for c, v in country_counts.items():
    if v <= q1:
        groups['Low'] += 1
    elif v <= q2:
        groups['Moderate'] += 1
    elif v <= q3:
        groups['High'] += 1
    else:
        groups['Very High'] += 1

# Heatmap: top 10 countries by top 8 currencies
top_countries = [c for c, _ in country_counts.most_common(10)]
top_currencies = [c for c, _ in currency_counts.most_common(8)]
country_currency = {c: Counter() for c in top_countries}
for r in rows:
    c = r['country']; cur = r['debt_amount']
    if c in country_currency and cur in top_currencies:
        country_currency[c][cur] += 1
matrix = [[country_currency[c][cur] for cur in top_currencies] for c in top_countries]

# generate charts
bar_chart_horizontal(
    'Top 15 Countries by Debt Record Volume',
    'Proxy for debt burden: number of debt records per country (dataset has no numeric amounts).',
    [c for c, _ in country_top15],
    [v for _, v in country_top15],
    os.path.join(OUT_DIR, 'top_countries_debt_burden.svg'),
    color='#1d4ed8'
)

bar_chart_horizontal(
    'Major Debt Resources (Currency Labels) in Dataset',
    'Most frequent debt_amount labels observed across all records.',
    [c for c, _ in currency_top12],
    [v for _, v in currency_top12],
    os.path.join(OUT_DIR, 'major_debt_resources.svg'),
    color='#7c3aed'
)

line_chart(
    'Debt Records Over Time (1995-2021)',
    'Annual frequency of debt records across all countries.',
    [str(y) for y in years],
    yvals,
    os.path.join(OUT_DIR, 'yearly_debt_records_trend.svg')
)

heatmap(
    'Country vs. Debt Resource Concentration',
    'Top 10 countries crossed with top 8 debt resource labels (counts).',
    top_countries,
    top_currencies,
    matrix,
    os.path.join(OUT_DIR, 'country_resource_heatmap.svg')
)

# summary text for README reuse
with open(os.path.join(OUT_DIR, 'summary_stats.txt'), 'w', encoding='utf-8') as f:
    f.write(f"Total records: {len(rows)}\n")
    f.write(f"Countries: {len(country_counts)}\n")
    f.write(f"Years: {min(years)}-{max(years)} ({len(years)} years)\n")
    f.write(f"Debt types: {dict(type_counts)}\n")
    f.write(f"Debt reasons: {dict(reason_counts)}\n")
    f.write(f"Debt status: {dict(status_counts)}\n")
    f.write("\nTop 15 countries by record volume:\n")
    for c, v in country_top15:
        f.write(f"- {c}: {v}\n")
    f.write("\nDebt burden groups (country count by quartile):\n")
    for g, v in groups.items():
        f.write(f"- {g}: {v}\n")

print('EDA artifacts generated in', OUT_DIR)
