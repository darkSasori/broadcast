#ifndef CONSUMER_H
#define CONSUMER_H

#include <QObject>

class Consumer : public QObject
{
    Q_OBJECT
public:
    explicit Consumer(QObject *parent = 0);

signals:

public slots:
};

#endif // CONSUMER_H
