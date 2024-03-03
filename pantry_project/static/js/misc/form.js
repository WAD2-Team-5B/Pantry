export class Form {
  /**
   * checks a set of conditions and displays an error message if any are true
   *
   * @param {SubmitEvent} event - the form submit event to prevent
   * @param {Array.<boolean>} errorConditions - the conditions to check
   * @param {HTMLElement} errorElement - the element to display the error message
   * @param {Array.<string>} errorMessages - the error messages to display
   */
  static validate(event, errorConditions, errorElement, errorMessages) {
    errorConditions.forEach((errorCondition) => {
      if (errorCondition) {
        errorElement.innerHTML =
          errorMessages[errorConditions.indexOf(errorCondition)];
        errorElement.className = "error-message-active";

        // stop form from submitting
        event.preventDefault();
        return false;
      }
    });
  }
}
