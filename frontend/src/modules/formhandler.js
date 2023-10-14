import { Modal } from 'flowbite';

class formTemplate {
    static standardAlert(message) {
        return `<div class="flex p-4 mb-4 text-sm text-yellow-700 bg-yellow-100 rounded-lg" role="alert">
              <svg aria-hidden="true" class="flex-shrink-0 inline w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
              <span class="sr-only">Info</span>
              <div>${message}</div>
            </div>`;
    }

    static dismissibleAlert(message) {
        return `<div id="alert" class="flex p-4 mb-4 bg-yellow-100 rounded-lg" role="alert">
                  <svg aria-hidden="true" class="flex-shrink-0 w-5 h-5 text-yellow-700" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                  <span class="sr-only">Info</span>
                  <div class="ml-3 text-sm font-medium text-yellow-700">${message}</div>
                  <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-yellow-100 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8" onclick="closeAlert(event)" aria-label="Close">
                    <span class="sr-only">Close</span>
                    <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                  </button>
                </div>`;
    }
}

// Get form data with submitter name and value.
function getFormData(e, form) {
    const data = new FormData(form);

    const { name, value } = e.submitter;
    data.append('submitter-name', name);
    data.append('submitter-value', value);

    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    data.append('csrfmiddlewaretoken', csrfToken);

    return data;
}

// Handle form submission and response.
async function handleFormSubmit(e, form) {
    try {
        const formData = getFormData(e, form);
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        if (!response.ok) {
            throw new Error('There was an error with your request, please try again.');
        }

        const responseData = await response.json();
        if (responseData.url) {
            window.location.replace(responseData.url);
        } else {
            displayResponseMessage(responseData, formData);
        }
    } catch (error) {
        console.error('Failed to submit form:', error);
        alert(error.message);
    }
}

// Displays a message in the form.
function displayFormErrors(form, errorMessage) {
    const messageEl = form.querySelector('.validity-message');
    if (!messageEl) {
        return;
    }

    const alertMessage = formTemplate.dismissibleAlert(errorMessage);
    messageEl.innerHTML += alertMessage;
    messageEl.focus();
}

// Displays a message in the specified container.
function displayResponseMessage(responseData, formData) {
    const responseContainer = document.getElementById(formData.get('response-container'));
    if (!responseContainer) {
        return;
    }
    const messageEl = responseContainer.querySelector('.response-message');
    if (!messageEl) {
        return;
    }

    const { status } = responseData;
    const messageType = status === 200 ? 'success' : 'error';
    const alertMessages =
        messageType === 'error'
            ? Object.entries(responseData.message || {}).map(([key, value]) =>
                  formTemplate.dismissibleAlert(`${key}: ${value}`)
              )
            : [formTemplate.standardAlert(responseData.message)];
    messageEl.innerHTML += alertMessages.join('');

    const responseHandler = formData.get('response-handler');
    if (responseHandler === 'modal') {
        getModal(responseContainer).show();
    } else {
        messageEl.focus();
    }
}

// Gets a modal with the specified backdrop class.
function getModal(modalContainer = document.body, backdropClass = 'modal-backdrop') {
    try {
        return new Modal(modalContainer, {
            backdropClasses: `${backdropClass} bg-gray-900 bg-opacity-50 fixed inset-0 z-40`,
        });
    } catch (error) {
        console.error('Failed to create modal:', error);
        return null;
    }
}

// Validates the form and returns true if valid.
function formValidate(e, form) {
    e.preventDefault();
    e.stopPropagation();

    const { name } = e.submitter;
    if (name === 'save') {
        const inputs = Array.from(form.querySelectorAll('input, select, textarea'));
        inputs.forEach((input) => {
            if (input.required) {
                input.required = false;
            }
        });
    }

    form.classList.add('was-validated');

    return !!form.checkValidity();
}

// Attaches event listeners to all forms with class "needs-validation" to handle form submissions.
function formHandler() {
    const validationForms = document.querySelectorAll('.needs-validation');
    Array.from(validationForms).forEach((form) => {
        const submitButtons = form.querySelectorAll('button[type="submit"]');
        form.addEventListener('submit', async (e) => {
            submitButtons.forEach((button) => {
                button.disabled = true;
                button.classList.add('cursor-not-allowed');
            });

            if (formValidate(e, form)) {
                await handleFormSubmit(e, form);
            } else {
                displayFormErrors(form, 'Please check the form for errors.');
            }

            setTimeout(() => {
                submitButtons.forEach((button) => {
                    button.disabled = false;
                    button.classList.remove('cursor-not-allowed');
                });
            }, 1000);
        });
    });
}

if (document.readyState !== 'loading') {
    formHandler();
} else {
    document.addEventListener('DOMContentLoaded', formHandler);
}

export default {
    formHandler,
};
