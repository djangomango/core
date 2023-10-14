function checkCKValid(ckInstanceName) {
  const instanceContainer = document.getElementById(ckInstanceName);
  let required = instanceContainer.getAttribute("data-required");
  let minLength = instanceContainer.getAttribute("minlength");
  let maxLength = instanceContainer.getAttribute("maxlength");

  const widgetContainer = document.getElementById(ckInstanceName + "_ckwidget");
  if (getCkValid(ckInstanceName, required, minLength, maxLength)) {
    validEl(widgetContainer);
  } else {
    invalidEl(widgetContainer);
  }
}

function getCkValid(ckInstanceName, required, minLength, maxLength) {
  let ckInstance = CKEDITOR.instances[ckInstanceName];
  let rawInput = ckInstance.getData();
  let trimInput = ckInstance.document.getBody().getText().trim();
  return !(
    (required && trimInput.length === 0) ||
    (minLength && rawInput.length < minLength) ||
    (maxLength && rawInput.length > maxLength)
  );
}

function validEl(el) {
  el.classList.remove("ck-invalid");
  el.classList.add("ck-valid");
}

function invalidEl(el) {
  el.classList.remove("ck-valid");
  el.classList.add("ck-invalid");
}

CKEDITOR.on("instanceReady", function () {
  for (const ckInstanceName in CKEDITOR.instances) {
    const ckInstance = CKEDITOR.instances[ckInstanceName];
    ckInstance.on("change", function () {
      ckInstance.updateElement();
      checkCKValid(ckInstanceName);
    });
    const ckInstanceForm = document.getElementById(ckInstanceName).form;
    ckInstanceForm.addEventListener("submit", function () {
      ckInstance.updateElement();
      checkCKValid(ckInstanceName);
    });
  }
});
