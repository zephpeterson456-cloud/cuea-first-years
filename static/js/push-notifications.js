document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("enable-notifications");

    if (!button || !("serviceWorker" in navigator) || !("PushManager" in window)) {
        return;
    }

    button.addEventListener("click", async () => {
        try {
            const permission = await Notification.requestPermission();

            if (permission !== "granted") {
                button.textContent = "🔕 Notifications blocked";
                return;
            }

            const registration = await navigator.serviceWorker.register(
                "/static/js/service-worker.js"
            );

            let subscription =
                await registration.pushManager.getSubscription();

            if (!subscription) {
                subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array(
                        button.dataset.publicKey
                    ),
                });
            }

            const response = await fetch("/push/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify(subscription),
            });

            if (response.ok) {
                button.textContent = "🔔 Notifications enabled";
                button.disabled = true;
            }
        } catch (error) {
            console.error("Push notification error:", error);
        }
    });
});

function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, "+")
        .replace(/_/g, "/");

    const rawData = window.atob(base64);
    return Uint8Array.from(
        [...rawData].map(char => char.charCodeAt(0))
    );
}

function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split("=");

        if (key === name) {
            return decodeURIComponent(value);
        }
    }

    return null;
}
