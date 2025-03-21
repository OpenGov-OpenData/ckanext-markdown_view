function render_md(url, target_element) {
  fetch(url)
    .then(response => response.text())
    .then(text => {
            converter = new showdown.Converter({
                'tables': true,
                'smoothLivePreview': true
            });
            html= converter.makeHtml(text);
            target_element.innerHTML = html;
  })
  .catch(console.error);
}


div = document.getElementById('md_view_html');
render_md(div.attributes['data-resource-url'].value, div);
