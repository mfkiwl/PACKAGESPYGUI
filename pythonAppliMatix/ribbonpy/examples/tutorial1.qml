import QtQuick 2.0

//http://doc.qt.io/qt-5/qml-tutorial1.html
//qmlscene tutorial1.qml

Rectangle {
    id: page
    width: 320; height: 480
    color: "lightgray"

    Text {
        id: helloText
        text: "Hello world!"
        y: 30
        anchors.horizontalCenter: page.horizontalCenter
        font.pointSize: 24; font.bold: true
    }
}

