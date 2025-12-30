import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import {UserContext} from "../context/userContextJS";

export default function ZeigtEingeben() {
    const { user } = useContext(UserContext);
    const navigate = useNavigate();

    const totalSquares = 60;                     // 6×10
    const filled = user.monaten.length;         // сколько квадратов должно быть зелёными

    // создаём массив из 60 элементов
    const squares = Array.from({ length: totalSquares }, (_, index) => ({
        isFilled: index < filled
    }));

    return (
        <div className="
        w-full
        min-h-[50svh]
        bg-gradient-to-b
        from-zinc-800
        to-black
        px-4
        pt-6
        ">

            <h1 className="text-2xl font-bold mb-4 text-center drop-shadow-[0_0_2px_white]">
                Deine Beiträge ({filled} Monate)
            </h1>

            {/* Сетка 10×6 */}
            <div className="grid grid-cols-6 gap-1 justify-center max-w-[260px] mx-auto">
                {squares.map((sq, index) => (
                    <div
                        key={index}
                        className={`
                            w-10 h-10 rounded 
                            border border-gray-700
                            ${sq.isFilled ? "bg-green-500" : "bg-gray-400"}
                        `}
                    >
                    </div>
                ))}
            </div>
            <div className='flex justify-center p-8'>
            <button
                onClick={() => navigate(-1)}
                className="w-[220px]
                max-w-xs
                py-4
                rounded-xl

                bg-gradient-to-br
                from-slate-100
                via-slate-400
                to-slate-700

                text-neutral-900
                text-lg
                font-semibold
                tracking-wide
                font-sans

                shadow-md
                shadow-black/30

    transition-all
    duration-300
    ease-out

    hover:from-teal-100
    hover:via-teal-500
    hover:to-teal-900

    active:scale-[0.98]
    active:from-teal-300
    active:to-teal-600
    "
            >
                ← Zurück
            </button>
            </div>
        </div>
    );
}
