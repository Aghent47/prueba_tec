const API_BASE_URL = "http://127.0.0.1:5000";

interface DocumentType {
  id: number;
  name: string;
}

interface UserData {
  document_number: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: number;
}

interface ApiResponse<T> {
  data: T | null;
  error?: {
    message: string;
    details?: string;
  };
}

/**
 * Obtener lista de tipos de documento desde el backend
 */
export async function getDocumentTypes(): Promise<DocumentType[]> {
  try {

    const response = await fetch(`${API_BASE_URL}/document-types`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const result: ApiResponse<DocumentType[]> = await response.json();
    return result.data || [];
  } catch (error) {
    console.error("Error fetching document types:", error);
    return [];
  }
}

/**
 * Buscar usuario por número de documento
 */
export async function searchUserByDNI(dniNumber: number): Promise<UserData | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/users/dni/${dniNumber}`);
    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const result: ApiResponse<UserData> = await response.json();
    return result.data;
  } catch (error) {
    console.error("Error searching user:", error);
    throw error;
  }
}
