import { Component, OnInit, ViewChild } from '@angular/core';
import { LDAModelService } from '../ldamodel/ldamodel.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  @ViewChild('navbar') navbar
  @ViewChild('burger') burger
  LDA_Models
  constructor(ldaModelService: LDAModelService) { 
    
    //Get LDA Models
    var promise = ldaModelService.getLDAModels()
    promise.then(
      (val) => this.LDA_Models = val,
      (err) => console.log(err)
    )

  }

  ngOnInit(): void {
    // Get all "navbar-burger" elements
    var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any nav burgers
    if ($navbarBurgers.length > 0) {

      // Add a click event on each of them
      $navbarBurgers.forEach(function ($el) {
        $el.addEventListener('click', function () {

          // Get the target from the "data-target" attribute
          var target = $el.dataset.target;
          var $target = document.getElementById(target);

          // Toggle the class on both the "navbar-burger" and the "navbar-menu"
          $el.classList.toggle('is-active');
          $target.classList.toggle('is-active');

        });
      });
    }

  }

  menuStatus: boolean = false;
  clickEvent() {
    this.menuStatus = !this.menuStatus;       
  }

  ngAfterViewInit() {
    var self = this
    this.navbar.nativeElement.addEventListener('click', function () {
      self.navbar.nativeElement.classList.remove("is-active")
      self.burger.nativeElement.classList.remove("is-active")
    });
  }
}