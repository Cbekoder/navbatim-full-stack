// Main JavaScript file for Navbatim.uz

import * as bootstrap from "bootstrap"

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Initialize popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl))

  // Add smooth scrolling to all links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href")
      if (targetId === "#") return

      const targetElement = document.querySelector(targetId)
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
        })
      }
    })
  })

  // Handle mobile navigation toggle
  const navbarToggler = document.querySelector(".navbar-toggler")
  if (navbarToggler) {
    navbarToggler.addEventListener("click", () => {
      const navbarMobile = document.getElementById("navbarMobile")
      if (navbarMobile.classList.contains("show")) {
        navbarMobile.classList.remove("show")
      } else {
        navbarMobile.classList.add("show")
      }
    })
  }

  // Handle filter accordion in catalog page
  const filterToggles = document.querySelectorAll(".filter-toggle")
  filterToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const target = document.getElementById(this.dataset.target)
      if (target) {
        if (target.classList.contains("show")) {
          target.classList.remove("show")
          this.querySelector("i").classList.remove("bi-chevron-up")
          this.querySelector("i").classList.add("bi-chevron-down")
        } else {
          target.classList.add("show")
          this.querySelector("i").classList.remove("bi-chevron-down")
          this.querySelector("i").classList.add("bi-chevron-up")
        }
      }
    })
  })
})
