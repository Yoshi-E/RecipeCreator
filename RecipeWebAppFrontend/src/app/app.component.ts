import { Component, OnInit, Inject} from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { Title, Meta } from '@angular/platform-browser';
import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer} from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent  implements OnInit {

  constructor(@Inject(DOCUMENT) private document: Document,
              private metaService: Meta) {}

  ngOnInit() {
    this.document.documentElement.lang = 'de'; 
    this.metaService.addTags([
      {name: 'charset', content: "UTF-8"},
      {name: 'content', content: 'de'}
    ]);
  }
}

@Pipe({ name: 'safe' })
export class SafePipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}
  transform(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
} 