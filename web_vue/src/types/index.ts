export const conclusions = {
  agreed: "СОГЛАСОВАНО",
  comments: "СОГЛАСОВАНО С КОММЕНТАРИЕМ",
  cancel: "СНЯТ С ПРОВЕРКИ",
  denied: "ОТКАЗАНО В СОГЛАСОВАНИИ",
};

export const decisions = {
  agreed: "БЕЗ ЗАМЕЧАНИЙ",
  comments: "С КОММЕНТАРИЯМИ",
  cancel: "ОТКАЗ ОТ ПРОВЕРКИ",
  denied: "НЕГАТИВ",
};

export interface TableColumns<T> {
  name: keyof T;
  header: string;
  cell?: (row: T) => string;
}

export interface ItemField<T> {
  key: keyof T;
  label: string;
  slot?: boolean;
  div?: (row: T) => string;
  component?: (row: T) => string;
}

export interface FormField<T> {
  element: "input" | "select" | "textarea";
  key: keyof T;
  label: string;
  attrs?: {
    [K in
      | "pattern"
      | "type"
      | "required"
      | "name"
      | "disabled"
      | "placeholder"
      | "autofocus"
      | "max"
      | "maxlength"
      | "min"
      | "minlength"]?: any;
  };
  items?: string[];
}

export interface Person {
  id: string;
  surname: string;
  firstname: string;
  patronymic?: string;
  birthday: string;
  birthplace?: string;
  citizenship?: string;
  dual?: string;
  snils?: string;
  inn?: string;
  marital?: string;
  addition?: string;
  destination?: string;
  editable: boolean;
  created: string;
  user_id: string;
}

export interface Previous {
  id: string;
  surname?: string;
  firstname?: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}
export interface Education {
  id: string;
  view?: string;
  institution: string;
  finished?: string;
  specialty: string;
}

export interface Staff {
  id: string;
  position: string;
  department?: string;
}

export interface Passport {
  id: string;
  view: string;
  series?: string;
  digits: string;
  agency?: string;
  issue: string;
}

export interface Address {
  id: string;
  view: string;
  address: string;
}

export interface Contact {
  id: string;
  view: string;
  contact: string;
}

export interface Work {
  id: string;
  starts: string;
  finished: string;
  workplace: string;
  address?: string;
  reason?: string;
  position: string;
}

export interface Affilation {
  id: string;
  view: string;
  organization: string;
  inn?: string;
  activity?: string;
}

export interface Verification {
  id: string;
  workplace?: string;
  document?: string;
  debt?: string;
  bankruptcy?: string;
  bki?: string;
  courts?: string;
  affilation?: string;
  terrorist?: string;
  internet?: string;
  cronos?: string;
  addition?: string;
  conclusion: string;
  comment?: string;
  created: string;
}

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion: string;
  created: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  created: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  origins?: string;
  created: string;
}

export interface Items {
  addresses: Address[];
  affilations: Affilation[];
  checks: Verification[];
  contacts: Contact[];
  documents: Passport[];
  educations: Education[];
  inquiries: Needs[];
  investigations: Inquisition[];
  poligrafs: Pfo[];
  previous: Previous[];
  staffs: Staff[];
  workplaces: Work[];
}
