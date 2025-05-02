import { Chart } from "@/components/ui/chart"
/**
 * Business Dashboard JavaScript
 * For Navbatim.uz
 */

document.addEventListener("DOMContentLoaded", () => {
  // Toggle sidebar on mobile
  const sidebarToggler = document.querySelector(".sidebar-toggler")
  const sidebar = document.querySelector(".sidebar")
  const mainContent = document.querySelector(".main-content")

  if (sidebarToggler) {
    sidebarToggler.addEventListener("click", () => {
      sidebar.classList.toggle("active")
      mainContent.classList.toggle("sidebar-active")
    })
  }

  // Initialize tooltips if Bootstrap is available
  if (typeof bootstrap !== "undefined") {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl))
  }

  // Initialize charts if Chart.js is available
  if (typeof Chart !== "undefined") {
    // Appointments Chart
    const appointmentsChartEl = document.getElementById("appointmentsChart")
    if (appointmentsChartEl) {
      const appointmentsChart = new Chart(appointmentsChartEl, {
        type: "line",
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          datasets: [
            {
              label: "Appointments",
              data: [65, 59, 80, 81, 56, 55, 40, 45, 60, 70, 75, 80],
              fill: false,
              borderColor: "#10b981",
              tension: 0.1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      })
    }

    // Revenue Chart
    const revenueChartEl = document.getElementById("revenueChart")
    if (revenueChartEl) {
      const revenueChart = new Chart(revenueChartEl, {
        type: "bar",
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          datasets: [
            {
              label: "Revenue",
              data: [12500, 15000, 17500, 16000, 19000, 21000, 22000, 24000, 23000, 25000, 27000, 30000],
              backgroundColor: "#f59e0b",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      })
    }

    // Services Chart
    const servicesChartEl = document.getElementById("servicesChart")
    if (servicesChartEl) {
      const servicesChart = new Chart(servicesChartEl, {
        type: "doughnut",
        data: {
          labels: ["Haircut", "Manicure", "Pedicure", "Facial", "Massage", "Other"],
          datasets: [
            {
              label: "Services",
              data: [30, 20, 15, 10, 15, 10],
              backgroundColor: ["#10b981", "#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6", "#6b7280"],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      })
    }
  }

  // Handle appointment filtering
  const appointmentFilterForm = document.getElementById("appointmentFilterForm")
  if (appointmentFilterForm) {
    appointmentFilterForm.addEventListener("submit", function (e) {
      e.preventDefault()
      const formData = new FormData(this)
      const params = new URLSearchParams()

      for (const [key, value] of formData.entries()) {
        if (value) {
          params.append(key, value)
        }
      }

      window.location.href = `${window.location.pathname}?${params.toString()}`
    })
  }

  // Handle client search
  const clientSearchInput = document.getElementById("clientSearch")
  if (clientSearchInput) {
    clientSearchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase()
      const clientRows = document.querySelectorAll(".client-row")

      clientRows.forEach((row) => {
        const clientName = row.querySelector(".client-name").textContent.toLowerCase()
        const clientPhone = row.querySelector(".client-phone").textContent.toLowerCase()
        const clientEmail = row.querySelector(".client-email").textContent.toLowerCase()

        if (clientName.includes(searchTerm) || clientPhone.includes(searchTerm) || clientEmail.includes(searchTerm)) {
          row.style.display = ""
        } else {
          row.style.display = "none"
        }
      })
    })
  }

  // Helper function to show alerts
  window.showAlert = (message, type = "success") => {
    const alertsContainer = document.getElementById("alertsContainer")
    if (!alertsContainer) return

    const alert = document.createElement("div")
    alert.className = `alert alert-${type} alert-dismissible fade show`
    alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `

    alertsContainer.appendChild(alert)

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      alert.classList.remove("show")
      setTimeout(() => {
        alertsContainer.removeChild(alert)
      }, 150)
    }, 5000)
  }

  // Helper function to get CSRF token
  window.getCsrfToken = () => document.querySelector('meta[name="csrf-token"]').getAttribute("content")

  // Helper function to format status text
  window.formatStatus = (status) => {
    const statusMap = {
      pending: "Pending",
      confirmed: "Confirmed",
      completed: "Completed",
      cancelled: "Cancelled",
    }

    return statusMap[status] || status.charAt(0).toUpperCase() + status.slice(1)
  }
})
