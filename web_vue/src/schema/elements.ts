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
  slot: "person",
} as ItemsAccordionTabs;

export const itemsTabs = [
  { label: "Проверки", slot: "checks" },
  { label: "Полиграф", slot: "poligrafs" },
  { label: "Расследования", slot: "investigations" },
  { label: "Запросы", slot: "inquiries" },
] as ItemsAccordionTabs[];

export const itemsAccordion = [
  { label: "Должности", slot: "staffs" },
  { label: "Образование", slot: "educations" },
  { label: "Места работы", slot: "workplaces" },
  { label: "Документы", slot: "documents" },
  { label: "Адреса", slot: "addresses" },
  { label: "Контакты", slot: "contacts" },
  { label: "Изменения имени", slot: "previous" },
  { label: "Аффилированность", slot: "affilations" },
] as ItemsAccordionTabs[];
