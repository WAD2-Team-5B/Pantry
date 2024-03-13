export const SPACER = "<SPACER>";

export class Form {
  /**
   * checks a set of conditions and displays an error message if any are true
   *
   * @param {SubmitEvent} event - the form submit event to prevent
   * @param {Array.<Object>} errorConditions - each object contains 'condition' and 'message' fields
   * @param {HTMLElement} errorElement - the element to display the error message
   */
  static validate(event, errorConditions, errorElement) {
    for (const errorCondition of errorConditions) {
      // check condition
      if (errorCondition.condition) {
        errorElement.innerHTML = errorCondition.message;
        errorElement.className = "error-message-active";

        // stop form from submitting
        event.preventDefault();
        return false;
      }
    }
  }

  /**
   * assigns values to a set of hidden inputs
   *
   * @param {Array.<Object>} hiddenInputs - each object contains 'input' and 'value' fields
   */
  static assignHiddenInputs(hiddenInputs) {
    for (const hiddenInput of hiddenInputs) {
      hiddenInput.input.value = hiddenInput.value.join(SPACER);
    }
  }
}
