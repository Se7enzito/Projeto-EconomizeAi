// Mostrar senha
var senha = $('#senha');
var olho = $("#olho");

olho.click(function() {
  var type = senha.attr("type") === "password" ? "text" : "password";
  senha.attr("type", type);
});

var cSenha = $("#cSenha");
var cOlho = $("#cOlho");

cOlho.click(function() {
  var type = cSenha.attr("type") === "password" ? "text" : "password";
  cSenha.attr("type", type);
});