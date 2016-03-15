import Colors from 'material-ui/lib/styles/colors';
import ColorManipulator from 'material-ui/lib/utils/color-manipulator';
import Spacing from 'material-ui/lib/styles/spacing';
import zIndex from 'material-ui/lib/styles/zIndex';

export default {
  spacing: Spacing,
  zIndex: zIndex,
  fontFamily: 'Roboto, sans-serif',
  palette: {
    primary1Color: "#0093ee",
    primary2Color: "#00baf6",
    primary3Color: "#00e7fb",
    accent1Color: "#11a982",
    accent2Color: "#333",
    accent3Color: "#444",
    textColor: "#000",
    alternateTextColor: "#fff",
    canvasColor: "#fff",
    borderColor: "#333",
    disabledColor: ColorManipulator.fade("#000", 0.3),
    pickerHeaderColor: "#0093ee",
  }
};