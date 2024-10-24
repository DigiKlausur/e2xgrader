import { IE2xCell } from '../base/base.interfaces';

export interface IChoiceCell extends IE2xCell {
  setChoices: (choices: string[]) => void;
  getChoices: () => string[];
}
