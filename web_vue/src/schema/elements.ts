import { localStr, timeAgoStr } from "@/utils";
import type {
  ItemFields,
  ItemsAccordionTabs,
  Person,
  TableColumns,
  User,
} from "@/types";

export const userCols: TableColumns<User>[] = [
  { name: "id", header: "#" },
  { name: "fullname", header: "Пользователь" },
  { name: "username", header: "Логин" },
  { name: "role", header: "Роль" },
  {
    name: "created",
    header: "Создан",
    cell: (row) => localStr(row.created),
  },
];

export const userDivs: ItemFields<User>[] = [
  { key: "fullname", label: "Пользователь" },
  { key: "username", label: "Логин" },
  { key: "role", label: "Роль" },
  {
    key: "created",
    label: "Создан",
    div: (row) => localStr(row.created),
  },
  { key: "attempt", label: "Попыток", div: (row) => String(row.attempt) },
  {
    key: "blocked",
    label: "Блокир.",
    div: (row) => (row.blocked ? "Да" : "Нет"),
  },
  {
    key: "change_pswd",
    label: "Пароль",
    div: (row) => (row.change_pswd ? "Да" : "Нет"),
  },
  {
    key: "deleted",
    label: "Удален",
    div: (row) => (row.deleted ? "Да" : "Нет"),
  },
];

export const personCols: TableColumns<Person>[] = [
  {
    name: "id",
    header: "#",
  },
  {
    name: "surname",
    header: "Фамилия",
  },
  {
    name: "firstname",
    header: "Имя",
  },
  {
    name: "patronymic",
    header: "Отчество",
  },
  {
    name: "birthday",
    header: "Дата рождения",
    cell: (row) => localStr(row.birthday),
  },
  {
    name: "created",
    header: "Обновлено",
    cell: (row) => timeAgoStr(row.created),
  },
];

export const anketaTab = {
  label: "Анкета",
  icon: "i-mi-user",
  slot: "person",
} as ItemsAccordionTabs;

export const itemsTabs = [
  {
    label: "Проверки",
    icon: "i-mi-document-check",
    slot: "checks",
  },
  {
    label: "Полиграф",
    icon: "i-mi-heart",
    slot: "poligrafs",
  },
  {
    label: "Расследования",
    icon: "i-mi-archive",
    slot: "investigations",
  },
  {
    label: "Запросы",
    icon: "i-mi-comment",
    slot: "inquiries",
  },
] as ItemsAccordionTabs[];

export const itemsAccordion = [
  {
    label: "Должности",
    icon: "i-mi-laptop",
    slot: "staffs",
  },
  {
    label: "Образование",
    icon: "i-mi-document-empty",
    slot: "educations",
  },
  {
    label: "Места работы",
    icon: "i-mi-computer",
    slot: "workplaces",
  },
  {
    label: "Документы",
    icon: "i-mi-document",
    slot: "documents",
  },
  {
    label: "Адреса",
    icon: "i-mi-home",
    slot: "addresses",
  },
  {
    label: "Контакты",
    icon: "i-mi-call",
    slot: "contacts",
  },
  {
    label: "Изменения имени",
    icon: "i-mi-edit",
    slot: "previous",
  },
  {
    label: "Аффилированность",
    icon: "i-mi-users",
    slot: "affilations",
  },
] as ItemsAccordionTabs[];
