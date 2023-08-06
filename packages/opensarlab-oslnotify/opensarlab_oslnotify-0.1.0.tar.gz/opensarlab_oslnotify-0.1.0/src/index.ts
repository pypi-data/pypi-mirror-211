import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';
import toastr from 'toastr';

interface IButter {
  title: string;
  message: string;
  type: string;
  severity: Partial<number>;
}

interface IBread {
  options: object;
  data: Array<IButter>;
}

function makeToast(notes: IBread) {
  toastr.options = notes.options;
  notes.data.forEach((entry: any) => {
    (toastr as any)[entry.type](entry.message, entry.title);
  });
}

function notifications(types: string) {
  document.head.insertAdjacentHTML(
    'beforeend',
    "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css'/>"
  );
  document.head.insertAdjacentHTML(
    'beforeend',
    '<style>#toast-container>div{opacity:1;}</style>'
  );

  requestAPI<any>(types)
    .then(notes => {
      makeToast(notes);
    })
    .catch(reason => {
      console.error(`Error oslnotify: ${reason}`);
    });
}

/**
 * Initialization data for the oslnotify extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'opensarlab-oslnotify:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension opensarlab-oslnotify is activated!');
    notifications('storage,calendar');
  }
};

export default plugin;
