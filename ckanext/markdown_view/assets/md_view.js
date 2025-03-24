function render_md(url, target_element) {
  fetch(url)
    .then(response => response.text())
    .then(text => {
            converter = new markdownit({
                html: false,   // Allow HTML tags in Markdown
                linkify: true, // Auto-detect links
                typographer: true // Convert quotes to typographic symbols
            });
            converter.use(window.markdownitFootnote);
            converter.use(window.markdownItAttrs);
            html= converter.render(text);
            target_element.innerHTML = html;
  })
  .catch(console.error);
}


div = document.getElementById('md_view_html');
render_md(div.attributes['data-resource-url'].value, div);
