import { LabIcon } from '@jupyterlab/ui-components';

import toggleOnSvgstr from '../../style/icons/toggle_on.svg';
import toggleOffSvgstr from '../../style/icons/toggle_off.svg';

export const toggleOnIcon = new LabIcon({
  name: 'toggle-on',
  svgstr: toggleOnSvgstr
});

export const toggleOffIcon = new LabIcon({
  name: 'toggle-off',
  svgstr: toggleOffSvgstr
});
