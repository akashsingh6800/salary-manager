import api from "../api";

export const getSummary = async () => {
    const response = await api.get("/analytics/summary");
    return response.data
}

export const getCountryAnalytics = async () => {
    const response = await api.get("/analytics/by-country");
    return response.data;
}

export const getDepartmentAnalytics = async () => {
    const response = await api.get("/analytics/by-department");
    return response.data;
}

export const getEmployees = async (
    page = 1,
    pageSize = 10,
    search = "",
) => {
    const response = await api.get("/employees", {
        params: {
            page,
            page_size: pageSize,
            search: search || undefined,
        },
    });
    return response.data;
}

export const getEmployee = async (employeeId: string) => {
    const response = await api.get(`/employees/${employeeId}`);
    return response.data;
}

export const getSalaryHistory = async (employeeId: string) => {
    const response = await api.get(
        `\employees/${employeeId}/salary-history`,
    );
    return response.data;

}

export const updateSalary = async (
    employeeId: string,
    data: {
        salary: number;
        currency: string;
        effective_from: string;
    },

) => {
    const response = await api.put(
        `/employees/${employeeId}/salary`,
        data
    );

    return response.data;

}

