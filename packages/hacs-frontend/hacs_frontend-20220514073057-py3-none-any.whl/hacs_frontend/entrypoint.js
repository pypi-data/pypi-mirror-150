
try {
  new Function("import('/hacsfiles/frontend/main-2af83765.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-2af83765.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  