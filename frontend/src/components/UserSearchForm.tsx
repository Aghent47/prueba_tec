import { useState, useEffect } from "react";
import { getDocumentTypes, searchUserByDNI } from "../services/api";
import SearchIcon from "./SearchIcon";

import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

interface DocumentType {
  id: number;
  name: string;
}

interface UserResult {
  document_number: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: number;
}

export default function UserSearchForm() {
  const [documentTypes, setDocumentTypes] = useState<DocumentType[]>([]);
  const [selectedDocType, setSelectedDocType] = useState<number | "">("");
  const [dniNumber, setDniNumber] = useState<string>("");
  const [searchResult, setSearchResult] = useState<UserResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  // Cargar tipos de documento al montar el componente
  useEffect(() => {
    const loadDocumentTypes = async () => {
      const types = await getDocumentTypes();
      setDocumentTypes(types);
    };
    loadDocumentTypes();
  }, []);

  // Manejar búsqueda
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSearchResult(null);

    if (!selectedDocType || !dniNumber) {
      setError("Por favor completa todos los campos");
      return;
    }

    setLoading(true);
    try {
      const result = await searchUserByDNI(Number(dniNumber));
      if (result) {
        setSearchResult(result);
      } else {
        setError("Usuario no encontrado");
      }
    } catch (err) {
      setError("Error al buscar el usuario");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Funciones de exportación
  const exportToExcel = () => {
    if (!searchResult) return;
    
    const data = [
      {
        "Nombre": searchResult.first_name,
        "Apellido": searchResult.last_name,
        "Documento": searchResult.document_number,
        "Email": searchResult.email,
        "Teléfono": searchResult.phone
      }
    ];

    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Usuario");
    XLSX.writeFile(workbook, `Usuario_${searchResult.document_number}.xlsx`);
  };

  const exportToCSV = () => {
    if (!searchResult) return;

    const data = [
      {
        "Nombre": searchResult.first_name,
        "Apellido": searchResult.last_name,
        "Documento": searchResult.document_number,
        "Email": searchResult.email,
        "Teléfono": searchResult.phone
      }
    ];

    const worksheet = XLSX.utils.json_to_sheet(data);
    const csvOutput = XLSX.utils.sheet_to_csv(worksheet);
    const blob = new Blob([csvOutput], { type: "text/csv;charset=utf-8" });
    saveAs(blob, `Usuario_${searchResult.document_number}.csv`);
  };

  const exportToTXT = () => {
    if (!searchResult) return;

    const content = `INFORMACIÓN DE USUARIO
----------------------
Nombre: ${searchResult.first_name}
Apellido: ${searchResult.last_name}
Documento: ${searchResult.document_number}
Email: ${searchResult.email}
Teléfono: ${searchResult.phone}
----------------------
Generado el: ${new Date().toLocaleString()}
`;

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    saveAs(blob, `Usuario_${searchResult.document_number}.txt`);
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-2xl animate-slide-up space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl sm:text-4xl font-bold text-gradient tracking-tight">
            Búsqueda de Usuarios
          </h1>
          <p className="text-white/60 font-light text-sm sm:text-base">
            Consulta información detallada por documento
          </p>
        </div>

        {/* Search Form Card */}
        <div className="glass-card-strong rounded-2xl p-6 sm:p-8 shadow-2xl ring-1 ring-white/10">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-teal-500/10 rounded-lg">
              <SearchIcon className="w-5 h-5 text-teal-400" />
            </div>
            <h2 className="text-xl font-semibold text-white">Nueva Búsqueda</h2>
          </div>

          <form onSubmit={handleSearch} className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              {/* Document Type */}
              <div className="space-y-2">
                <label htmlFor="docType" className="block text-xs font-medium text-white/70 uppercase tracking-wider">
                  Tipo de Documento
                </label>
                <div className="relative">
                  <select
                    id="docType"
                    value={selectedDocType}
                    onChange={(e) => setSelectedDocType(Number(e.target.value) || "")}
                    className="w-full bg-white/5 border border-white/10 text-white rounded-xl px-4 py-3
                             focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20
                             transition-all duration-200 hover:bg-white/10
                             text-sm appearance-none cursor-pointer"
                    style={{ colorScheme: 'dark' }}
                  >
                    <option value="" className="bg-gray-900">Seleccionar...</option>
                    {documentTypes.map((type) => (
                      <option key={type.id} value={type.id} className="bg-gray-900">
                        {type.name}
                      </option>
                    ))}
                  </select>
                  <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-white/40">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Document Number */}
              <div className="space-y-2">
                <label htmlFor="dniNumber" className="block text-xs font-medium text-white/70 uppercase tracking-wider">
                  Número de Documento
                </label>
                <input
                  id="dniNumber"
                  type="number"
                  value={dniNumber}
                  onChange={(e) => setDniNumber(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 text-white rounded-xl px-4 py-3
                           focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20
                           transition-all duration-200 hover:bg-white/10
                           text-sm placeholder-white/20"
                  placeholder="Ej: 12345678"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-400 hover:to-cyan-500
                       text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-teal-500/20
                       transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
                       transform hover:-translate-y-0.5 active:translate-y-0
                       flex items-center justify-center gap-2 text-sm sm:text-base"
            >
              {loading ? (
                <>
                  <span className="spinner w-4 h-4 border-2" aria-hidden></span>
                  <span>Procesando...</span>
                </>
              ) : (
                <>
                  <span>Buscar Usuario</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="animate-slide-up">
            <div className="bg-red-500/10 border border-red-500/20 text-red-200 rounded-xl p-4 flex items-center gap-3 backdrop-blur-sm">
              <div className="p-2 bg-red-500/20 rounded-full shrink-0">
                <svg className="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p className="text-sm font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Results Section */}
        {searchResult && (
          <div className="animate-slide-up">
            <div className="glass-card-strong rounded-2xl overflow-hidden shadow-2xl ring-1 ring-white/10">
              {/* Result Header */}
              <div className="bg-white/5 p-6 sm:p-8 border-b border-white/5 flex flex-col sm:flex-row items-center gap-6">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-teal-400 to-cyan-600 flex items-center justify-center shadow-lg shadow-teal-500/20 shrink-0 text-2xl font-bold text-white">
                  {searchResult.first_name.charAt(0)}{searchResult.last_name.charAt(0)}
                </div>
                <div className="text-center sm:text-left space-y-1">
                  <h3 className="text-2xl font-bold text-white">
                    {searchResult.first_name} {searchResult.last_name}
                  </h3>
                  <div className="flex items-center justify-center sm:justify-start gap-2">
                    <span className="px-2.5 py-0.5 rounded-full bg-teal-500/20 text-teal-300 text-xs font-medium border border-teal-500/20">
                      Verificado
                    </span>
                    <span className="text-white/40 text-sm">•</span>
                    <span className="text-white/60 text-sm">ID: {searchResult.document_number}</span>
                  </div>
                </div>
              </div>

              {/* Result Details */}
              <div className="p-6 sm:p-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-white/5 border border-white/5 space-y-1 hover:bg-white/10 transition-colors">
                  <p className="text-xs font-medium text-white/50 uppercase tracking-wider">Correo Electrónico</p>
                  <p className="text-white font-medium truncate">{searchResult.email}</p>
                </div>
                <div className="p-4 rounded-xl bg-white/5 border border-white/5 space-y-1 hover:bg-white/10 transition-colors">
                  <p className="text-xs font-medium text-white/50 uppercase tracking-wider">Teléfono</p>
                  <p className="text-white font-medium">{searchResult.phone}</p>
                </div>
              </div>

              {/* Actions */}
              <div className="p-6 bg-white/5 border-t border-white/5 flex flex-wrap justify-center gap-3">
                <button
                  onClick={exportToExcel}
                  className="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-white/80 text-sm font-medium transition-all hover:text-white flex items-center gap-2"
                >
                  <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Excel
                </button>
                <button
                  onClick={exportToCSV}
                  className="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-white/80 text-sm font-medium transition-all hover:text-white flex items-center gap-2"
                >
                  <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  CSV
                </button>
                <button
                  onClick={exportToTXT}
                  className="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-white/80 text-sm font-medium transition-all hover:text-white flex items-center gap-2"
                >
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  TXT
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
