import { localStr, timeAgoStr } from "@/utils";
import type { ItemsAccordionTabs, Person, TableColumns } from "@/types";

export const tableCols: TableColumns<Person>[] = [
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
