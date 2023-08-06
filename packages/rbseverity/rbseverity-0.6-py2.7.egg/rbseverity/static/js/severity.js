"use strict";

window.RBSeverity = {};
/**
 * Extends the comment dialog to provide buttons for severity.
 *
 * The Save button will be removed, and in its place will be a set of
 * buttons for choosing the severity level for the comment. The buttons
 * each work as save buttons.
 */

RBSeverity.CommentDialogHookView = Backbone.View.extend({
  events: {
    'click .buttons .save-major': '_onSaveMajorClicked',
    'click .buttons .save-minor': '_onSaveMinorClicked',
    'click .buttons .save-info': '_onSaveInfoClicked'
  },
  buttonsTemplate: _.template("<span class=\"severity-actions\">\n  <input type=\"button\" class=\"save-major\" value=\"Major\"\n         disabled=\"true\" />\n  <input type=\"button\" class=\"save-minor\" value=\"Minor\"\n         disabled=\"true\" />\n  <input type=\"button\" class=\"save-info\" value=\"Info\"\n         disabled=\"true\" />\n</span>"),

  /**
   * Initialize the view.
   *
   * Args:
   *     options (object):
   *         Options for the view.
   *
   * Option Args:
   *     commentDialog (RB.CommentDialogView):
   *         The comment dialog.
   *
   *     commentEditor (RB.CommentEditor):
   *         The comment editor model.
   */
  initialize: function initialize(options) {
    this.commentDialog = options.commentDialog;
    this.commentEditor = options.commentEditor;
  },

  /**
   * Render the additions to the comment dialog.
   *
   * This will remove the Save button and set up the new buttons.
   */
  render: function render() {
    var $severityButtons = $(this.buttonsTemplate());
    this.commentDialog.$saveButton.remove();
    this.commentDialog.$buttons.prepend($severityButtons);
    $severityButtons.find('input').bindVisibility(this.commentEditor, 'canEdit').bindProperty('disabled', this.commentEditor, 'canSave', {
      elementToModel: false,
      inverse: true
    });
    /* Set a default severity, in case the user hits Control-Enter. */

    this.commentEditor.setExtraData('severity', 'info');
  },

  /**
   * Handler for when the "Major" button is clicked.
   *
   * Saves the comment with a "Major" severity.
   */
  _onSaveMajorClicked: function _onSaveMajorClicked() {
    this._saveCommon('major');
  },

  /**
   * Handler for when the "Minor" button is clicked.
   *
   * Saves the comment with a "Minor" severity.
   */
  _onSaveMinorClicked: function _onSaveMinorClicked() {
    this._saveCommon('minor');
  },

  /**
   * Handler for when the "Info" button is clicked.
   *
   * Saves the comment with an "Info" severity.
   */
  _onSaveInfoClicked: function _onSaveInfoClicked() {
    this._saveCommon('info');
  },

  /**
   * Common function for saving with a severity.
   *
   * This will set the severity for the comment and then save it.
   *
   * Args:
   *     severity (string):
   *         The severity to set.
   */
  _saveCommon: function _saveCommon(severity) {
    if (this.commentEditor.get('canSave')) {
      this.commentEditor.setExtraData('severity', severity);
      this.commentDialog.save();
    }
  }
});
/**
 * Extends the review dialog to allow setting severities on unpublished
 * comments.
 *
 * A field will be provided that contains a list of severities to choose
 * from.
 *
 * If the comment does not have any severity set yet (meaning it's a pending
 * comment from before the extension was activated), a blank entry will be
 * added. If the severity is then set, the blank entry will go away the next
 * time it's loaded.
 */

RBSeverity.ReviewDialogCommentHookView = Backbone.View.extend({
  events: {
    'change select': '_onSeverityChanged'
  },
  template: _.template("<label for=\"<%- id %>\">Severity:</label>\n<select id=\"<%- id %>\">\n <option value=\"major\">Major</option>\n <option value=\"minor\">Minor</option>\n <option value=\"info\">Info</option>\n</select>"),

  /**
   * Render the editor for a comment's severity.
   *
   * Returns:
   *     RBSeverity.ReviewDialogCommentHookView:
   *     This object, for chaining.
   */
  render: function render() {
    var severity = this.model.get('extraData').severity;
    this.$el.html(this.template({
      id: 'severity_' + this.model.id
    }));
    this._$select = this.$('select');

    if (severity) {
      this._$select.val(severity);
    } else {
      this._$select.prepend($('<option selected/>'));
    }

    return this;
  },

  /**
   * Handler for when the severity is changed by the user.
   *
   * Updates the severity on the comment to match.
   */
  _onSeverityChanged: function _onSeverityChanged() {
    this.model.get('extraData').severity = this._$select.val();
    this.model.save();
  }
});
/**
 * Extends Review Board with comment severity support.
 *
 * This plugs into the comment dialog and review dialog to add the ability
 * to set severities for comments.
 */

RBSeverity.Extension = RB.Extension.extend({
  /**
   * Initialize the JavaScript extension.
   */
  initialize: function initialize() {
    RB.Extension.prototype.initialize.call(this);
    new RB.CommentDialogHook({
      extension: this,
      viewType: RBSeverity.CommentDialogHookView
    });
    new RB.ReviewDialogCommentHook({
      extension: this,
      viewType: RBSeverity.ReviewDialogCommentHookView
    });
  }
});

//# sourceMappingURL=severity.js.map