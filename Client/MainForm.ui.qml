import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

Item {
    width: 640
    height: 480

    property alias btnRED: btnRED
    property alias btnGREEN: btnGREEN
    property alias btnBLUE: btnBLUE

    RowLayout {
        anchors.centerIn: parent

        RadioButton {
            id: btnRED
            text: qsTr("RED")
        }

        RadioButton {
            id: btnGREEN
            text: qsTr("GREEN")
        }

        RadioButton {
            id: btnBLUE
            text: qsTr("BLUE")
        }
    }
}
