import dayjs from "dayjs";
import { useState } from "react";
import localeData from "dayjs/plugin/localeData"
import "dayjs/locale/de"
import ToggleMonatenButton  from "./ToggleMonatenButton.jsx";
import {useContext} from "react";
import {UserContextJS} from "../context/userContextJS.js";
import ShowButton from "./ShowButton.jsx";

dayjs.extend(localeData)
dayjs.locale("de")


export default function AddMonaten(){
    const [year, setYear] = useState(dayjs().year());

    const months = dayjs.months(); // ['January', 'February', ...]

    const { user, openModal, setMonaten } = useContext(UserContextJS);

    function nextYear() {
        setYear(prev => prev + 1);
    }

    function prevYear() {
        setYear(prev => prev - 1);
    }

    function toggleMonth(month, year) {

        setMonaten(prev => {
            const exists = prev.some(
                m => m.year === year && m.month === month
            );

            let updated;

            if (exists) {
                updated = prev.filter(
                    m => !(m.year === year && m.month === month)
                );
            } else {
                updated = [...prev, { year, month }];
            }

            // Проверка лимита
            if (!exists && updated.length === 4) {
                openModal("Поздравляем! Вы собрали 4 взноса (тест).");
            }

            return updated;  // ← НЕ объект, только массив
        });
    }


    console.log('Что такое юзер - ', user);  // весь объект
    console.log('Что у юзера в месяцах - ', user.monaten); // 0
    return (

        <div className='w-full
        min-h-[50svh]
        bg-gradient-to-b
        from-zinc-800
        to-black
        px-4
        pt-6
        '>
            <p className="text-3xl font-bold text-center
            text-gray-300 mt-4 mb-2
             tracking-wide">{year}</p>
            <div className='flex justify-center'>
                <div className="grid grid-cols-3 gap-2 p-4">
                    {months.map(month => (
                        <ToggleMonatenButton
                            key={`${year}-${month}`}
                            label={month}
                            year={year}
                            isActive={user.monaten.some(m => m.year === year && m.month === month)}
                            toggleMonth={toggleMonth}
                        />
                    ))}
                </div>
            </div>
            <div className='flex justify-center'>
                <button
                    disabled={year <= 2015}
                    className={`w-[120px] h-[56px] m-2 rounded-lg
        text-neutral-100 font-extrabold text-2xl

        bg-gradient-to-br
        from-slate-300 
        to-slate-600

        transition-all duration-300

        hover:from-green-300
        hover:to-emerald-900

        active:scale-[0.97]
                    ${year <= 2015 ? "opacity-40" : ''}`}
                    onClick={prevYear}>←
                </button>
                <button
                    disabled={year >= 2040}
                    className={`w-[120px] h-[56px] m-2 rounded-lg
        text-neutral-100 font-extrabold text-2xl

        bg-gradient-to-br
        from-slate-300
        to-slate-600

        transition-all duration-300

        hover:from-green-300
        hover:to-emerald-900

        active:scale-[0.97]
                    ${year >= 2040 ? "opacity-40" : ""}`} onClick={nextYear}>→
                </button>
            </div>
            <div className='flex justify-center mt-8'>
                <ShowButton/>
            </div>
        </div>
    );
}