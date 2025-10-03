import cairosvg

def counts(project_id: str):
    return {"identified": 0, "after_dedup": 0, "screened": 0, "included": 0, "excluded": 0}

def figure_png(project_id: str, out_svg: str, out_png: str, counts_dict: dict):
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
      <rect x="50" y="50" width="300" height="60" fill="#eee" stroke="#333"/>
      <text x="60" y="90" font-size="16">Records identified: {counts_dict['identified']}</text>

      <rect x="50" y="150" width="300" height="60" fill="#eee" stroke="#333"/>
      <text x="60" y="190" font-size="16">After dedup: {counts_dict['after_dedup']}</text>

      <rect x="50" y="250" width="300" height="60" fill="#eee" stroke="#333"/>
      <text x="60" y="290" font-size="16">Screened: {counts_dict['screened']}</text>

      <rect x="50" y="350" width="300" height="60" fill="#eee" stroke="#333"/>
      <text x="60" y="390" font-size="16">Included: {counts_dict['included']}</text>

      <rect x="400" y="250" width="300" height="60" fill="#eee" stroke="#333"/>
      <text x="410" y="290" font-size="16">Excluded: {counts_dict['excluded']}</text>
    </svg>
    """
    with open(out_svg, "w", encoding="utf-8") as f: f.write(svg)
    cairosvg.svg2png(url=out_svg, write_to=out_png)
