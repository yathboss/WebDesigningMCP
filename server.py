import json
import os
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with a clean name
mcp = FastMCP("Vibe Design Guide")

# Load database path relative to this script
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "guide_db.json")

def load_db() -> dict:
    """Helper function to load the structured design guide database."""
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Fallback empty structure if file is missing
        return {}

@mcp.tool()
def list_design_elements() -> str:
    """
    List all available design elements in the guide, grouped by category.
    Categories include aesthetics, scroll animations, layouts, navigation patterns,
    typography rules, and UI components.
    """
    db = load_db()
    if not db:
        return "Error: Could not load the design guide database."
        
    result = []
    category_labels = {
        "aesthetics": "1. Design Aesthetics",
        "scroll_animation": "2. Scroll & Animation",
        "layouts": "3. Layouts",
        "navigation": "4. Navigation",
        "typography_color": "5. Typography & Color",
        "ui_patterns": "6. UI Patterns"
    }
    
    for cat_key, label in category_labels.items():
        if cat_key in db:
            result.append(f"### {label}")
            elements = db[cat_key]
            for elem_key, elem_data in elements.items():
                title = elem_data.get("title", elem_key)
                result.append(f"- **{title}** (`{elem_key}`)")
            result.append("")
            
    return "\n".join(result)

@mcp.tool()
def get_element_details(category: str, name: str) -> str:
    """
    Get detailed information, explanations, CSS guidelines, study examples, 
    and copy-paste prompting templates for a specific design element.
    
    Args:
        category: Must be one of: aesthetics, scroll_animation, layouts, navigation, typography_color, ui_patterns
        name: The key identifier of the element (e.g. 'glassmorphism', 'bento_grid', 'pricing_table')
    """
    db = load_db()
    if not db:
        return "Error: Could not load the design guide database."
        
    if category not in db:
        valid_cats = ", ".join(db.keys())
        return f"Error: Category '{category}' not found. Valid categories are: {valid_cats}"
        
    category_data = db[category]
    if name not in category_data:
        valid_names = ", ".join(category_data.keys())
        return f"Error: Design element '{name}' not found in category '{category}'. Valid names are: {valid_names}"
        
    data = category_data[name]
    
    output = []
    output.append(f"# {data.get('title')}")
    output.append(f"**Category**: {category.replace('_', ' ').title()}\n")
    
    if "what_it_is" in data:
        output.append(f"## What it is\n{data['what_it_is']}\n")
        
    if "how_it_works" in data:
        output.append(f"## How it works\n{data['how_it_works']}\n")
        
    if "css_properties" in data:
        output.append("## CSS Guidelines")
        output.append("```css")
        props = data["css_properties"]
        if isinstance(props, dict):
            for k, v in props.items():
                output.append(f"{k}: {v};")
        elif isinstance(props, list):
            for item in props:
                output.append(f"/* {item} */")
        else:
            output.append(str(props))
        output.append("```\n")
        
    if "pairings" in data:
        output.append("## Recommended Pairings")
        for k, v in data["pairings"].items():
            output.append(f"- **{k.replace('_', ' ').title()}**: {v}")
        output.append("")
        
    if "distribution" in data:
        output.append("## Color Distribution Guide")
        for k, v in data["distribution"].items():
            output.append(f"- **{k.replace('_', ' ').title()}**: {v}")
        output.append("")
        
    if "key_elements" in data:
        output.append("## Key Structure Elements")
        for item in data["key_elements"]:
            output.append(f"- {item}")
        output.append("")
        
    if "tips" in data:
        output.append("## Best Practice Tips")
        for item in data["tips"]:
            output.append(f"- {item}")
        output.append("")
        
    if "ai_prompt" in data:
        output.append("## AI Prompt to Use")
        output.append(f"> \"{data['ai_prompt']}\"\n")
        
    if "examples" in data:
        output.append("## Example Websites to Study")
        for ex in data["examples"]:
            output.append(f"- {ex}")
            
    return "\n".join(output)

@mcp.tool()
def search_guide(query: str) -> str:
    """
    Search the entire Vibe Coder Design Guide for visual aesthetics, layout patterns,
    animation code, or UI elements matching a keyword.
    
    Args:
        query: The search term (e.g. 'box-shadow', 'retro', 'sticky', 'pricing')
    """
    db = load_db()
    if not db:
        return "Error: Could not load the design guide database."
        
    query = query.lower()
    results = []
    
    for cat_key, elements in db.items():
        for elem_key, elem_data in elements.items():
            # Search title, what_it_is, how_it_works, and prompt
            title = elem_data.get("title", "").lower()
            what = elem_data.get("what_it_is", "").lower()
            how = elem_data.get("how_it_works", "").lower()
            prompt = elem_data.get("ai_prompt", "").lower()
            
            if query in title or query in what or query in how or query in prompt or query in elem_key.lower():
                category_name = cat_key.replace("_", " ").title()
                results.append(f"- **{elem_data.get('title')}** in *{category_name}* (`get_element_details(category='{cat_key}', name='{elem_key}')`)")
                snippet = elem_data.get("what_it_is", "")[:120]
                if len(elem_data.get("what_it_is", "")) > 120:
                    snippet += "..."
                results.append(f"  > {snippet}")
                results.append("")
                
    if not results:
        return f"No results found for query '{query}'."
        
    return f"### Search Results for '{query}':\n\n" + "\n".join(results)

@mcp.tool()
def compose_design_prompt(
    aesthetic: Optional[str] = None,
    layout: Optional[str] = None,
    animation: Optional[str] = None,
    colors: Optional[str] = None,
    typography: Optional[str] = None,
    custom_request: Optional[str] = None
) -> str:
    """
    Compose a structured, highly optimized front-end prompt using the Vibe Coder's formula:
    Aesthetic + Layout + Animation + specific colors and fonts + custom requests.
    
    Args:
        aesthetic: Key of the aesthetic (e.g. 'glassmorphism', 'neumorphism', 'brutalism', 'dark_luxury')
        layout: Key of the layout (e.g. 'hero_feature_grid', 'bento_grid', 'asymmetric_split')
        animation: Key of the animation (e.g. 'scroll_triggered_animations', 'parallax_scrolling', 'text_reveal')
        colors: Description of custom colors or hex codes (e.g. '#667eea to #764ba2')
        typography: Specific font choices or font pairings (e.g. 'Clash Display + Satoshi')
        custom_request: Any additional details of sections or features you want to build
    """
    db = load_db()
    if not db:
        return "Error: Could not load the design guide database."
        
    # 1. Gather Aesthetic Details
    aesthetic_info = ""
    aesthetic_prompt_part = ""
    if aesthetic:
        a_data = db.get("aesthetics", {}).get(aesthetic)
        if a_data:
            aesthetic_info = f"- **Aesthetic**: {a_data['title']} ({a_data['what_it_is']})\n"
            aesthetic_prompt_part = f"Style with a refined {a_data['title']} aesthetic. "
            if "css_properties" in a_data:
                props = a_data["css_properties"]
                prop_details = []
                if isinstance(props, dict):
                    for k, v in props.items():
                        if k != "colors":
                            prop_details.append(f"{k}: {v}")
                if prop_details:
                    aesthetic_prompt_part += f"Implement it using exact CSS attributes: {', '.join(prop_details)}. "
        else:
            aesthetic_info = f"- **Aesthetic**: {aesthetic} (Custom)\n"
            aesthetic_prompt_part = f"Use a {aesthetic} style. "
            
    # 2. Gather Layout Details
    layout_info = ""
    layout_prompt_part = ""
    if layout:
        l_data = db.get("layouts", {}).get(layout)
        if l_data:
            layout_info = f"- **Layout**: {l_data['title']} ({l_data['what_it_is']})\n"
            layout_prompt_part = f"Arrange elements in a {l_data['title']} configuration. "
            if "css_properties" in l_data:
                props = l_data["css_properties"]
                prop_details = [f"{k}: {v}" for k, v in props.items()] if isinstance(props, dict) else []
                if prop_details:
                    layout_prompt_part += f"Construct this using CSS layout declarations: {', '.join(prop_details)}. "
        else:
            layout_info = f"- **Layout**: {layout} (Custom)\n"
            layout_prompt_part = f"Arrange in a {layout} layout. "
            
    # 3. Gather Animation Details
    animation_info = ""
    animation_prompt_part = ""
    if animation:
        an_data = db.get("scroll_animation", {}).get(animation)
        if an_data:
            animation_info = f"- **Animation**: {an_data['title']} ({an_data['what_it_is']})\n"
            animation_prompt_part = f"Add {an_data['title']} animations. "
            if "css_properties" in an_data:
                props = an_data["css_properties"]
                prop_details = [f"{k}: {v}" for k, v in props.items()] if isinstance(props, dict) else []
                if prop_details:
                    animation_prompt_part += f"Use animation characteristics: {', '.join(prop_details)}. "
        else:
            animation_info = f"- **Animation**: {animation} (Custom)\n"
            animation_prompt_part = f"Add smooth {animation} scroll/entry animation. "
            
    # 4. Assemble colors and fonts
    style_details = []
    if colors:
        style_details.append(f"Color palette: {colors}")
    if typography:
        style_details.append(f"Typography: {typography}")
        
    style_prompt_part = ""
    if style_details:
        style_prompt_part = f"Apply these styling tokens: {', '.join(style_details)}. "
        
    # 5. Custom Requirements
    custom_prompt_part = ""
    if custom_request:
        custom_prompt_part = f"\nSpecific requirements to build: {custom_request}"
        
    # Assemble the final prompt
    composed_prompt = (
        f"Create a modern, responsive web application component with the following specifications:\n\n"
        f"1. AESTHETIC: {aesthetic_prompt_part.strip()}\n"
        f"2. LAYOUT: {layout_prompt_part.strip()}\n"
        f"3. ANIMATION: {animation_prompt_part.strip()}\n"
        f"4. STYLING: {style_prompt_part.strip()}\n"
        f"{custom_prompt_part.strip()}\n\n"
        f"Provide semantic, clean HTML5 code and vanilla, modern CSS (with custom properties if applicable) "
        f"incorporating transitions and clean micro-interactions. If JavaScript is needed for triggers, "
        f"use concise, standard ES6 code."
    )
    
    result = [
        "## Composed Front-End Prompt",
        "Copy and paste the prompt below into your AI builder (like Stitch, v0, Bolt, or Framer):",
        "```text",
        composed_prompt.strip(),
        "```",
        "",
        "### Composition Meta Details",
        aesthetic_info.strip(),
        layout_info.strip(),
        animation_info.strip(),
        f"- **Custom Colors**: {colors if colors else 'Not specified'}",
        f"- **Custom Typography**: {typography if typography else 'Not specified'}"
    ]
    
    return "\n".join(result)

if __name__ == "__main__":
    # Start the fastmcp server
    mcp.run()
