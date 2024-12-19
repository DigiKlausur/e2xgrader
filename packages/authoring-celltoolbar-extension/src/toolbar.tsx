import {
  HTMLSelect,
  InputGroup,
  ReactWidget,
  Toolbar,
  ToolbarButton
} from '@jupyterlab/ui-components';
import { Cell } from '@jupyterlab/cells';
import {
  showAuthoringToolbarSignal,
  hideAuthoringToolbarSignal
} from './signals';
import { ICellRegistry } from '@e2xgrader/cell-core';
import * as React from 'react';
import { Message } from '@lumino/messaging';
import { GradingCell, getAvailableCellTypes } from './model';
import { toggleOnIcon, toggleOffIcon } from './icon';
import VisibilitySingleton from './visibility';

export const E2X_TOOLBAR_CLASS = 'e2x-authoring-toolbar';
export const E2X_TOOLBAR_STANDARD_CELL_CLASS =
  'e2x-authoring-toolbar-standard-cell';
export const E2X_TOOLBAR_GRADING_CELL_CLASS =
  'e2x-authoring-toolbar-grading-cell';
export const E2X_TOOLBAR_ELEMENT_CLASS = 'e2x-authoring-toolbar-element';

export class AuthoringCellToolbar extends Toolbar {
  _cell: Cell | undefined = undefined;
  _model: GradingCell | undefined = undefined;
  _visibility: VisibilitySingleton = VisibilitySingleton.getInstance();
  cellRegistry: ICellRegistry;
  constructor(cellRegistry: ICellRegistry) {
    super();
    this.cellRegistry = cellRegistry;
    this.addClass(E2X_TOOLBAR_CLASS);
    if (this._visibility.isVisible) {
      this.show();
    } else {
      this.hide();
    }
    showAuthoringToolbarSignal.connect(this.show, this);
    hideAuthoringToolbarSignal.connect(this.hide, this);
    this.switchToStandardCellHighlighting();
  }

  switchToStandardCellHighlighting() {
    this.removeClass(E2X_TOOLBAR_GRADING_CELL_CLASS);
    this.addClass(E2X_TOOLBAR_STANDARD_CELL_CLASS);
  }

  switchToGradingCellHighlighting() {
    this.removeClass(E2X_TOOLBAR_STANDARD_CELL_CLASS);
    this.addClass(E2X_TOOLBAR_GRADING_CELL_CLASS);
  }

  getCell(): Cell {
    return this._cell as Cell;
  }

  getModel(): GradingCell {
    return this._model as GradingCell;
  }

  protected onAfterAttach(_msg: Message): void {
    this._cell = this.parent as Cell;
    this._model = new GradingCell(this._cell);
    this.updateChildren();
  }

  update(): void {
    super.update();
    this.updateChildren();
  }

  updateChildren() {
    Array.from(this.children()).forEach(child => {
      if (child instanceof AuthoringCellToolbar.HeaderElement) {
        child.update();
      }
    });
  }
}

export namespace AuthoringCellToolbar {
  export class HeaderElement extends ReactWidget {
    toolbar: AuthoringCellToolbar;
    modelReady: boolean;
    constructor(toolbar: AuthoringCellToolbar) {
      super();
      this.addClass(E2X_TOOLBAR_ELEMENT_CLASS);
      this.toolbar = toolbar;
      this.modelReady = false;
    }

    getCell(): Cell {
      return this.toolbar.getCell();
    }

    getModel(): GradingCell {
      return this.toolbar.getModel();
    }

    renderElement(): React.JSX.Element {
      return <></>;
    }

    render(): React.ReactElement | null {
      if (this.getModel()) {
        this.modelReady = true;
        return this.renderElement();
      } else {
        return null;
      }
    }
  }

  export class GradeIDInput extends HeaderElement {
    gradeId: string | undefined;

    update(): void {
      this.gradeId = this.getModel().model.gradeId;
      super.update();
    }

    setGradeId(gradeId: string) {
      this.gradeId = gradeId;
      this.getModel().model.gradeId = gradeId;
      this.update();
    }

    renderElement() {
      if (!this.gradeId) {
        return <></>;
      }
      return (
        <>
          <label htmlFor="grade-id">Grade ID:</label>
          <InputGroup
            id="grade-id"
            aria-label="Grade ID"
            placeholder="Grade ID"
            className="e2x-grade-id-input"
            value={this.gradeId}
            onChange={event => {
              this.setGradeId(event.currentTarget.value);
            }}
          />
        </>
      );
    }
  }

  export class PointsInput extends HeaderElement {
    points: number | undefined;

    update(): void {
      this.points = this.getModel().model.points;
      super.update();
    }

    setPoints(points: number) {
      this.points = points;
      this.getModel().model.points = points;
      this.update();
    }

    renderElement() {
      if (this.points === undefined) {
        return <></>;
      }
      return (
        <>
          <label htmlFor="points">Points:</label>
          <InputGroup
            id="points"
            type="number"
            placeholder="Points"
            className="e2x-points-input"
            min={0}
            value={this.points}
            onChange={event => {
              this.setPoints(Number(event.currentTarget.value));
            }}
          />
        </>
      );
    }
  }

  export class GradingCellTypeSelect extends HeaderElement {
    cellType: string | undefined;
    availableTypes: string[][] = [['', '-']];

    setCellType(cellType: string) {
      this.cellType = cellType;
      this.getModel().setGradingCellType(this.cellType);
      this.update();
    }

    update(): void {
      this.cellType = this.getModel().model.gradingCellType ?? '';
      if (this.cellType === '') {
        this.toolbar.switchToStandardCellHighlighting();
      } else {
        this.toolbar.switchToGradingCellHighlighting();
      }
      this.availableTypes = getAvailableCellTypes(
        this.getCell(),
        this.toolbar.cellRegistry
      );
      super.update();
    }

    renderElement() {
      return (
        <>
          <label htmlFor="grading-cell-type">Type:</label>
          <HTMLSelect
            id="grading-cell-type"
            options={
              this.availableTypes.map(([value, label]) => {
                return { value, label };
              }) ?? []
            }
            value={this.cellType}
            onChange={event => {
              this.setCellType(event.currentTarget.value);
              this.toolbar.update();
            }}
          />
        </>
      );
    }
  }

  export function createToggleAuthoringToolbarButton(): ToolbarButton {
    const visibilityManager = VisibilitySingleton.getInstance();
    const toggleToolbarButton = new ToolbarButton({
      label: 'Toggle Authoring Toolbar',
      icon: toggleOffIcon,
      pressedIcon: toggleOnIcon,
      pressed: visibilityManager.isVisible,
      onClick: function () {
        visibilityManager.setVisibility(!toggleToolbarButton.pressed);
      }
    });
    showAuthoringToolbarSignal.connect(() => {
      toggleToolbarButton.pressed = true;
    });
    hideAuthoringToolbarSignal.connect(() => {
      toggleToolbarButton.pressed = false;
    });
    return toggleToolbarButton;
  }

  export function createAuthoringToolbar(
    cellRegistry: ICellRegistry
  ): AuthoringCellToolbar {
    const toolbar = new AuthoringCellToolbar(cellRegistry);
    toolbar.addItem('spacer', Toolbar.createSpacerItem());
    toolbar.addItem('points', new PointsInput(toolbar));
    toolbar.addItem('grade-id', new GradeIDInput(toolbar));
    toolbar.addItem('grading-cell-type', new GradingCellTypeSelect(toolbar));
    return toolbar;
  }
}
