import { useEffect, useState } from "react";
import {
  AppBar,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Toolbar,
  Typography,
  Pagination,
  Button
} from "@mui/material";

import {
  getCountryAnalytics,
  getDepartmentAnalytics,
  getSummary,
  getEmployees,
  getEmployee,
  getSalaryHistory,
  updateSalary
} from "./services/api";


function App() {
  const [summary, setSummary] = useState({
    total_employees: 0,
    active_employees: 0,
    total_countries: 0,
    total_departments: 0,
  });

  const [countries, setCountries] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [search, setSearch] = useState("");

  const [employees, setEmployees] = useState<any[]>([]);
  const [totalEmployees, setTotalEmployees] = useState(0);
  const [page, setPage] = useState(1);
  const [loadingEmployees, setLoadingEmployees] = useState(false);


  const [selectedEmployee, setSelectedEmployee] = useState<any | null>(null);
  const [salaryHistory, setSalaryHistory] = useState<any[]>([]);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [salary, setSalary] = useState("");
  const [currency, setCurrency] = useState("");
  const [effectiveFrom, setEffectiveFrom] = useState("");
  const [updatingSalary, setUpdatingSalary] = useState(false);


  const handleEmployeeClick = async (employeeId: string) => {
    try {
      setLoadingDetails(true);
  
      const [employee, history] = await Promise.all([
        getEmployee(employeeId),
        getSalaryHistory(employeeId),
      ]);
  
      setSelectedEmployee(employee);
      setSalaryHistory(history);
    } catch (error) {
      console.error("Failed to load employee details:", error);
    } finally {
      setLoadingDetails(false);
    }
  };

  const handleSalaryUpdate = async () => {
    if (!selectedEmployee) {
      return;
    }
  
    try {
      setUpdatingSalary(true);
  
      await updateSalary(selectedEmployee.employee_id, {
        salary: Number(salary),
        currency: currency.toUpperCase(),
        effective_from: effectiveFrom,
      });
  
      const history = await getSalaryHistory(
        selectedEmployee.employee_id
      );
  
      setSalaryHistory(history);
  
      setSalary("");
      setCurrency("");
      setEffectiveFrom("");
    } catch (error) {
      console.error("Failed to update salary:", error);
    } finally {
      setUpdatingSalary(false);
    }
  };

  useEffect(() => {
    

    const loadDashboard = async () => {
      try {
        const [summaryData, countryData, departmentData] =
          await Promise.all([
            getSummary(),
            getCountryAnalytics(),
            getDepartmentAnalytics(),
          ]);

        setSummary(summaryData);
        setCountries(countryData);
        setDepartments(departmentData);
      } catch (error) {
        console.error("Failed to load dashboard:", error);
      }
    };

    loadDashboard();
  }, []);

  useEffect(() => {
    const loadEmployees = async () => {
      try {
        setLoadingEmployees(true);
  
        const data = await getEmployees(page, 10, search);
  
        setEmployees(data.items);
        setTotalEmployees(data.total);
      } catch (error) {
        console.error("Failed to load employees:", error);
      } finally {
        setLoadingEmployees(false);
      }
    };
  
    loadEmployees();
  }, [page, search]);

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f5f7fa" }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            ACME Salary Management
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 4 }}>
     
        <Typography variant="h4" sx={{ mb: 1 }}>
          HR Dashboard
        </Typography>

        <Typography color="text.secondary" sx={{ mb: 4 }}>
          Employee salary and compensation overview
        </Typography>

        <Grid container spacing={3}>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">
                  Total Employees
                </Typography>
                <Typography variant="h4">
                  {summary.total_employees}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">
                  Active Employees
                </Typography>
                <Typography variant="h4">
                  {summary.active_employees}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">
                  Countries
                </Typography>
                <Typography variant="h4">
                  {summary.total_countries}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">
                  Departments
                </Typography>
                <Typography variant="h4">
                  {summary.total_departments}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Box sx={{ mt: 5 }}>
          <TextField
            fullWidth
            label="Search employees"
            placeholder="Search by employee name, ID or email"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </Box>

        <Box sx={{ mt: 3 }}>
  <Card>
    <CardContent>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Employees
      </Typography>

      {loadingEmployees ? (
        <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer component={Paper} elevation={0}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Employee ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Country</TableCell>
                <TableCell>Department</TableCell>
                <TableCell>Job Title</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {employees.map((employee) => (
                <TableRow 
                key={employee.employee_id}
                hover
                onClick={()=> handleEmployeeClick(employee.employee_id)}
                sx={{cursor: "pointer"}}
                >
                  <TableCell>{employee.employee_id}</TableCell>

                  <TableCell>
                    {employee.first_name} {employee.last_name}
                  </TableCell>

                  <TableCell>{employee.email}</TableCell>

                  <TableCell>
                    {employee.country?.name || employee.country}
                  </TableCell>

                  <TableCell>
                    {employee.department?.name || employee.department}
                  </TableCell>

                  <TableCell>{employee.job_title}</TableCell>

                  <TableCell>
                    {employee.employment_status}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ mt: 2 }}
      >
        Showing {employees.length} of {totalEmployees} employees
      </Typography>
      <Pagination
      count = {Math.ceil(totalEmployees/10)}
      page = {page}
      onChange={(_,value)=> setPage(value)}
      sx={{mt:2, display: "flex",justifyContent: "center"}}
      />
    </CardContent>
  </Card>
</Box>


{selectedEmployee && (
  <Typography>SELECTED EMPLOYEE LOADED</Typography>
)}

{selectedEmployee && (
  <Box sx={{ mt: 3 }}>
    <Card>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 3 }}>
          Employee Details
        </Typography>

        {loadingDetails ? (
          <Box sx={{ display: "flex", justifyContent: "center", py: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <Grid container spacing={3}>
              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Employee ID
                </Typography>
                <Typography>
                  {selectedEmployee.employee_id}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Name
                </Typography>
                <Typography>
                  {selectedEmployee.first_name}{" "}
                  {selectedEmployee.last_name}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Email
                </Typography>
                <Typography>
                  {selectedEmployee.email}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Country
                </Typography>
                <Typography>
                  {selectedEmployee.country}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Department
                </Typography>
                <Typography>
                  {selectedEmployee.department}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Job Title
                </Typography>
                <Typography>
                  {selectedEmployee.job_title}
                </Typography>
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                <Typography color="text.secondary">
                  Employment Status
                </Typography>
                <Typography>
                  {selectedEmployee.employment_status}
                </Typography>
              </Grid>
            </Grid>

            <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
              Salary History
            </Typography>

            {salaryHistory.length === 0 ? (
              <Typography color="text.secondary">
                No salary history available.
              </Typography>
            ) : (
              <TableContainer component={Paper} elevation={0}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Salary</TableCell>
                      <TableCell>Currency</TableCell>
                      <TableCell>Effective From</TableCell>
                    </TableRow>
                  </TableHead>

                  <TableBody>
                    {salaryHistory.map((salary, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          {Number(salary.salary).toLocaleString()}
                        </TableCell>
                        <TableCell>
                          {salary.currency}
                        </TableCell>
                        <TableCell>
                          {salary.effective_from}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
            <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
  Update Salary
</Typography>

<Grid container spacing={2}>
  <Grid size={{ xs: 12, sm: 4 }}>
    <TextField
      fullWidth
      label="Salary"
      type="number"
      value={salary}
      onChange={(event) => setSalary(event.target.value)}
    />
  </Grid>

  <Grid size={{ xs: 12, sm: 4 }}>
    <TextField
      fullWidth
      label="Currency"
      value={currency}
      onChange={(event) => setCurrency(event.target.value)}
      inputProps={{ maxLength: 3 }}
    />
  </Grid>

  <Grid size={{ xs: 12, sm: 4 }}>
    <TextField
      fullWidth
      label="Effective From"
      type="date"
      value={effectiveFrom}
      onChange={(event) => setEffectiveFrom(event.target.value)}
      slotProps={{
        inputLabel: {
          shrink: true,
        },
      }}
    />
  </Grid>

  <Grid size={{ xs: 12 }}>
    <Button
      variant="contained"
      onClick={handleSalaryUpdate}
      disabled={
        updatingSalary ||
        !salary ||
        !currency ||
        !effectiveFrom
      }
    >
      {updatingSalary ? "Updating..." : "Update Salary"}
    </Button>
  </Grid>
</Grid>
          </>
        )}
      </CardContent>
    </Card>
  </Box>
)}


        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Salary by Country
                </Typography>

                {countries.map((item) => (
                  <Box
                    key={`${item.country}-${item.currency}`}
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      py: 1,
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    <Typography>{item.country}</Typography>
                    <Typography>
                      {item.currency}{" "}
                      {item.average_salary.toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Salary by Department
                </Typography>

                {departments.map((item) => (
                  <Box
                    key={`${item.department}-${item.currency}`}
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      py: 1,
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    <Typography>{item.department}</Typography>
                    <Typography>
                      {item.currency}{" "}
                      {item.average_salary.toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;