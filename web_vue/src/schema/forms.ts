import { Conclusions, Decisions } from "@/types";
import type { Items, FormFields } from "@/types";

const pattern = "^[А-ЯЁ][А-ЯЁ\\-.,' ]+[А-ЯЁ]$";

export const person = [
  {
    element: "input",
    key: "surname",
    label: "Фамилия",
    props: {
      pattern: pattern,
      placeholder: "Фамилия (заглавными буквами)",
      maxlength: 255,
      required: true,
    },
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
    props: {
      pattern: pattern,
      placeholder: "Имя (заглавными буквами)",
      maxlength: 255,
      required: true,
    },
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
    props: {
      pattern: pattern,
      placeholder: "Отчество (заглавными буквами)",
      maxlength: 255,
    },
  },
  {
    element: "input",
    key: "birthday",
    label: "Дата рождения",
    props: { type: "date", required: true },
  },
  {
    element: "input",
    key: "birthplace",
    label: "Место рождения",
    props: { placeholder: "Место рождения", maxlength: 255 },
  },
  {
    element: "input",
    key: "citizenship",
    label: "Гражданство",
    props: { placeholder: "Гражданство", maxlength: 255 },
  },
  {
    element: "input",
    key: "dual",
    label: "Двойное гражданство",
    props: { placeholder: "Двойное гражданство", maxlength: 255 },
  },
  {
    element: "input",
    key: "snils",
    label: "СНИЛС",
    props: { pattern: "^\\d{11}$", placeholder: "СНИЛС" },
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
    props: { pattern: "^\\d{12}$", placeholder: "ИНН" },
  },
  {
    element: "input",
    key: "marital",
    label: "Семейное положение",
    props: { placeholder: "Семейное положение", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительно",
    props: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
] as FormFields<Items["person"]>[];

const addresses = [
  {
    element: "select",
    key: "view",
    label: "Вид адреса",
    items: ["Адрес регистрации", "Адрес проживания", "Другое"],
    props: { placeholder: "Выберите адрес", required: true },
  },
  {
    element: "textarea",
    key: "address",
    label: "Адрес",
    props: { placeholder: "Введите адрес", maxlength: 4096, required: true },
  },
] as FormFields<Items["addresses"]>[];

const affilations = [
  {
    element: "input",
    key: "view",
    label: "Вид участия",
    props: { placeholder: "Вид участия", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "organization",
    label: "Организация",
    props: { placeholder: "Организация", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
    props: { placeholder: "Организация", pattern: "^\\d{10,12}$" },
  },
  {
    element: "textarea",
    key: "activity",
    label: "Деятельность",
    props: { placeholder: "Деятельность", maxlength: 4096 },
  },
] as FormFields<Items["affilations"]>[];

const checks = [
  {
    element: "textarea",
    key: "workplace",
    label: "Проверка по местам работы",
    props: { placeholder: "Проверка по местам работы", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "document",
    label: "Проверка документов",
    props: { placeholder: "Проверка документов", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "debt",
    label: "Проверка задолженностей",
    props: { placeholder: "Проверка задолженностей", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "bankruptcy",
    label: "Проверка банкротства",
    props: { placeholder: "Проверка банкротства", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "bki",
    label: "Проверка Кредитной истории",
    props: { placeholder: "Проверка Кредитной истории", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "courts",
    label: "Проверка судебных дел",
    props: { placeholder: "Проверка судебных дел", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "affilation",
    label: "Проверка аффилированности",
    props: { placeholder: "Проверка аффилированности", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "terrorist",
    label: "Проверка в списке террористов",
    props: { placeholder: "Проверка в списке террористов", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "internet",
    label: "Проверка в открытых источниках",
    props: { placeholder: "Проверка в открытых источниках", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "cronos",
    label: "Проверка в Кронос",
    props: { placeholder: "Проверка в Кронос", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительная информация",
    props: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "comment",
    label: "Комментарий",
    props: { placeholder: "Комментарий", maxlength: 4096 },
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    items: Object.values(Conclusions),
    props: { placeholder: "Выберите результат", required: true },
  },
] as FormFields<Items["checks"]>[];

const contacts = [
  {
    element: "select",
    key: "view",
    label: "Вид контакта",
    items: ["Телефон", "Электронная почта", "Другое"],
    props: {
      placeholder: "Выберите контакт",
      maxlength: 255,
      required: true,
    },
  },
  {
    element: "input",
    key: "contact",
    label: "Контакт",
    props: { placeholder: "Контакт", maxlength: 255, required: true },
  },
] as FormFields<Items["contacts"]>[];

const documents = [
  {
    element: "select",
    key: "view",
    label: "Вид документа",
    items: ["Паспорт", "Иностранный паспорт", "Другое"],
    props: { placeholder: "Выберите документ", required: true },
  },
  {
    element: "input",
    key: "series",
    label: "Серия",
    props: { placeholder: "Серия", maxlength: 16 },
  },
  {
    element: "input",
    key: "digits",
    label: "Номер",
    props: { placeholder: "Номер", maxlength: 16, required: true },
  },
  {
    element: "input",
    key: "agency",
    label: "Кем выдан",
    props: { placeholder: "Орган выдавший", maxlength: 255 },
  },
  {
    element: "input",
    key: "issue",
    label: "Дата выдачи",
    props: { type: "date", required: true },
  },
] as FormFields<Items["documents"]>[];

const educations = [
  {
    element: "select",
    key: "view",
    label: "Вид образования",
    items: [
      "Основное общее",
      "Среднее общее",
      "Среднее профессиональное",
      "Высшее",
      "Неоконченное высшее образование",
      "Другое образование",
    ],
    props: { placeholder: "Выберите образование", required: true },
  },
  {
    element: "input",
    key: "institution",
    label: "Учебное заведение",
    props: {
      placeholder: "Учебное заведение",
      maxlength: 255,
      required: true,
    },
  },
  {
    element: "input",
    key: "finished",
    label: "Год окончания",
    props: { placeholder: "Год окончания", pattern: "^\\d{4}$" },
  },
  {
    element: "input",
    key: "specialty",
    label: "Специальность",
    props: { placeholder: "Специальность", maxlength: 255, required: true },
  },
] as FormFields<Items["educations"]>[];

const inquiries = [
  {
    element: "textarea",
    key: "info",
    label: "Информация",
    props: { placeholder: "Информация", maxlength: 4096, required: true },
  },
  {
    element: "input",
    key: "initiator",
    label: "Инициатор",
    props: { placeholder: "Инициатор", maxlength: 255, required: true },
  },
] as FormFields<Items["inquiries"]>[];

const investigations = [
  {
    element: "input",
    key: "theme",
    label: "Тема проверки",
    props: { placeholder: "Тема проверки", maxlength: 255, required: true },
  },
  {
    element: "textarea",
    key: "info",
    label: "Информация",
    props: { placeholder: "Информация", maxlength: 4096, required: true },
  },
] as FormFields<Items["investigations"]>[];

const poligrafs = [
  {
    element: "select",
    key: "theme",
    label: "Тема проверки",
    items: [
      "Проверка кандидата",
      "Служебная проверка",
      "Служебное расследование",
      "Плановое мероприятие",
    ],
    props: { placeholder: "Выберите тему", required: true },
  },
  {
    element: "textarea",
    key: "results",
    label: "Результат",
    props: { placeholder: "Результат", maxlength: 4096, required: true },
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    items: Object.values(Decisions),
    props: { placeholder: "Выберите результат", required: true },
  },
] as FormFields<Items["poligrafs"]>[];

const previous = [
  {
    element: "input",
    key: "surname",
    label: "Фамилия",
    props: { placeholder: "Фамилия", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
    props: { placeholder: "Имя", maxlength: 255 },
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
    props: { placeholder: "Отчество", maxlength: 255 },
  },
  {
    element: "input",
    key: "changed",
    label: "Год изменения",
    props: { placeholder: "Год изменения", pattern: "^\\d{4}$" },
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина",
    props: { placeholder: "Причина изменения", maxlength: 4096 },
  },
] as FormFields<Items["previous"]>[];

const staffs = [
  {
    element: "input",
    key: "position",
    label: "Должность",
    props: { placeholder: "Должность", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "department",
    label: "Подразделение",
    props: { placeholder: "Подразделение", maxlength: 255 },
  },
] as FormFields<Items["staffs"]>[];

const workplaces = [
  {
    element: "input",
    key: "starts",
    label: "Начало работы",
    props: { type: "date", required: true },
  },
  {
    element: "input",
    key: "finished",
    label: "Окончание работы",
    props: { type: "date" },
  },
  {
    element: "input",
    key: "workplace",
    label: "Место работы",
    props: { placeholder: "Место работы", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "position",
    label: "Должность",
    props: { placeholder: "Должность", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "address",
    label: "Адрес организации",
    props: { placeholder: "Адрес организации", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина увольнения",
    props: { placeholder: "Причина увольнения", maxlength: 4096 },
  },
] as FormFields<Items["workplaces"]>[];

export const itemsForms = {
  addresses,
  affilations,
  checks,
  contacts,
  documents,
  educations,
  inquiries,
  investigations,
  person,
  poligrafs,
  previous,
  staffs,
  workplaces,
} as { [key in keyof Items]: FormFields<Items[keyof Items]>[] };
