import { useEffect, useState } from "react";


export function UserProvider({ children }) {

    const telegramId =
        window.Telegram?.WebApp?.initDataUnsafe?.user?.id?.toString() ?? null;

    const [monaten, setMonaten] = useState([]);

    const user = { // создаём юзера и запишем его в контекст
        id: telegramId,
        monaten
    };

    // --- Модалка ---
    const [modal, setModal] = useState({
        isOpen: false,
        message: ""
    });

    function openModal(message) {
        setModal({ isOpen: true, message });
    }

    function closeModal() {
        setModal({ isOpen: false, message: "" });
    }

    // --- Инициализация Telegram WebApp ---
    useEffect(() => {
        async function init() {
            if (!window.Telegram?.WebApp) {
                console.warn("Telegram WebApp не найден");
                return;
            }

            const initData = window.Telegram.WebApp.initDataUnsafe;

            console.log("📦 initData:", initData);

            if (!initData?.user?.id) {
                console.error("❌ В initData нет user.id");
                return;
            }

            try {
                const res = await fetch("api/receive_telegram_data", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_id: telegramId })
                });

                const data = await res.json();
                console.log("📨 Ответ сервера:", data);
            } catch (err) {
                console.error("❌ Ошибка отправки:", err);
            }

            // 3️⃣ сохраняем в localStorage (не обязательно)
            localStorage.setItem("telegramUserId", telegramId);
        }

        init();
    }, []);

    const wa = window.Telegram?.WebApp;
    const tgUser = wa?.initDataUnsafe?.user;

    // ❌ Открыто НЕ из Telegram
    if (!wa || !tgUser) {
        return (
            <div className="p-6 text-center">
                <h2 className="text-xl font-semibold mb-4">
                    🚫 Доступ ограничен
                </h2>

                <p className="mb-4">
                    Это веб-приложение можно использовать только через Telegram.
                </p>

                <a
                    href="https://t.me/buergerschaft_bot"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block mt-4 px-6 py-3 bg-blue-500 text-white rounded-md"
                >
                    👉 Открыть бота в Telegram
                </a>
            </div>
        );
    }

    return (
        <UserContext.Provider value={{
            user,
            setMonaten,
            modal,
            openModal,
            closeModal
        }}>
            {children}
        </UserContext.Provider>
    );
}



