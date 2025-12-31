import { useContext } from "react";
import {UserContextJS} from "../context/userContextJS.js";

export default function Modul() {
    const { modal, closeModal } = useContext(UserContextJS);

    if (!modal.isOpen) return null;

    return (
        <div className="modal-overlay" onClick={closeModal}>
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                <div className="bg-white p-6 rounded-xl shadow-xl max-w-xs text-center">

                    <p className="text-lg font-semibold mb-4">{modal.message}</p>

                    <button
                        onClick={closeModal}
                        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                        OK
                    </button>
                </div>
            </div>
        </div>
            );
            }
