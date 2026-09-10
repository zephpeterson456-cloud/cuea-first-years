self.addEventListener("push", event => {
    let data = {};

    try {
        data = event.data ? event.data.json() : {};
    } catch (error) {
        data = {
            title: "CUEA First Years Hub",
            body: event.data ? event.data.text() : "You have a new notification.",
        };
    }

    const title = data.title || "CUEA First Years Hub";

    const options = {
        body: data.body || "You have a new notification.",
        icon: data.icon || "/static/icons/icon-192.png",
        badge: data.badge || "/static/icons/icon-192.png",
        data: {
            url: data.url || "/",
        },
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener("notificationclick", event => {
    event.notification.close();

    const url = event.notification.data?.url || "/";

    event.waitUntil(
        clients.matchAll({
            type: "window",
            includeUncontrolled: true,
        }).then(windowClients => {
            for (const client of windowClients) {
                if ("focus" in client) {
                    client.navigate(url);
                    return client.focus();
                }
            }

            return clients.openWindow(url);
        })
    );
});
