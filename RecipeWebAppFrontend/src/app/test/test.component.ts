import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {

	name = "New User";
  counterService = 0;
  constructor() {  }

  get count() {
      return this.counterService
    }
  inc_count(){
      this.counterService += 1;
    }

  ngOnInit(): void {}
}
