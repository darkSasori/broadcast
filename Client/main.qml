import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2
//import Qt.WebSockets 1.0
import "WebSocket.js" 1.0 as WebSocketBroadcast

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    MainForm {
        anchors.fill: parent
        btnRED.onCheckedChanged:
            if( btnRED.checked )
                ws.sendTextMessage("{\"target\": \"r\", \"queue\": \"color\", \"value\": 255}");
            else
                ws.sendTextMessage("{\"target\": \"r\", \"queue\": \"color\", \"value\": 0}");

        btnGREEN.onCheckedChanged:
            if( btnGREEN.checked )
                ws.sendTextMessage("{\"target\": \"g\", \"queue\": \"color\", \"value\": 255}");
            else
                ws.sendTextMessage("{\"target\": \"g\", \"queue\": \"color\", \"value\": 0}");

        btnBLUE.onCheckedChanged:
            if( btnBLUE.checked )
                ws.sendTextMessage("{\"target\": \"b\", \"queue\": \"color\", \"value\": 255}");
            else
                ws.sendTextMessage("{\"target\": \"b\", \"queue\": \"color\", \"value\": 0}");

    }

    MessageDialog {
        id: messageDialog
        title: qsTr("WebSocket")

        function show(caption) {
            messageDialog.text = caption;
            messageDialog.open();
        }
    }
}
