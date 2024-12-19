import {
  //toggleAuthoringToolbarVisibilitySignal,
  hideAuthoringToolbarSignal,
  showAuthoringToolbarSignal
} from './signals';

class VisibilitySingleton {
  private static instance: VisibilitySingleton;
  public isVisible: boolean;

  private constructor() {
    this.isVisible = false;
  }

  setVisibility(isVisible: boolean) {
    this.isVisible = isVisible;
    if (isVisible) {
      showAuthoringToolbarSignal.emit();
    } else {
      hideAuthoringToolbarSignal.emit();
    }
  }

  public static getInstance(): VisibilitySingleton {
    if (!VisibilitySingleton.instance) {
      VisibilitySingleton.instance = new VisibilitySingleton();
    }
    return VisibilitySingleton.instance;
  }
}

export default VisibilitySingleton;
