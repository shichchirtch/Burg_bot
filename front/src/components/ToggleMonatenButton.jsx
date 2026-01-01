import { useContext } from "react";
import { UserContextJS } from "../context/userContextJS.js";

function ToggleMonatenButton({ label, year, isActive, toggleMonth }) {
    // const telegramId = localStorage.getItem("telegramUserId");
    const { user } = useContext(UserContextJS);
    // let user.id = telegramId
    // const telegramId = localStorage.getItem("telegramUserId");

    async function handleClick() {
        const newState = !isActive;

        if (isActive) {
            const ok = window.confirm(
                `Вы уверены, что хотите удалить ${label} ${year}?`
            );
            if (!ok) return;
        }

        // 1. Меняем локальное состояние
        toggleMonth(label, year);

        // 2. Шлём обновление на сервер
        try {
            await fetch("/api/month-select", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: user.id,
                    month: label,
                    year: year,
                    selected: newState,
                })
            });
        } catch (error) {
            console.error("Ошибка отправки:", error);
        }
    }
    return (
        <button
            onClick={handleClick }// toggleMonth(label, year)}
            className={`
        p-4 w-24 h-20 rounded-md
        text-xs font-semibold

        border-2 border-neutral-700

        transition-all duration-300
        active:scale-[0.96]

        ${isActive
                ? `
                text-neutral-50
                bg-gradient-to-br
                from-gray-300
                via-green-500
                to-teal-950
                shadow-md shadow-emerald-900/30
              `
                : `
                text-neutral-900
                bg-gradient-to-br
                from-slate-300 
                to-neutral-600
              `
            }
    `}
        >
            {label}
        </button>
    );
}

export default ToggleMonatenButton;
