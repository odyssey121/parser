import React, { PureComponent } from "react";
import { Icon, Table, Typography } from "antd";
const { Text } = Typography;

const placeholder = <Icon type="loading" style={{ fontSize: 44 }} spin />;

const ResultTable = ({ result, loading }) => {
  //   const renderTable = () => {
  //     if (result){

  //     }

  //   };

  const renderColumns = () => {
    return [
      {
        title: "Загаловок",
        dataIndex: "title",
        key: "title",
        width: "70%",
        render: title => <div>{title && title}</div>
        // sorter: (a, b) => {
        //   return a.title.localeCompare(b.title);
        // }
      },
      {
        title: "Ссылки на контент",
        dataIndex: "linkContent",
        key: "linkContent",
        width: "20%",
        render: linkContent => (
          <div>
            {linkContent && linkContent.map(link => <a href={link}>{link}</a>)}
          </div>
        )
        // sorter: (a, b) => {
        //   return a.content.localeCompare(b.content);
        // }
      },
      {
        title: "Дата",
        dataIndex: "date",
        key: "date",
        width: "10",
        render: date => <div>{date && date}</div>
        // sorter: (a, b) => {
        //   return a.date.localeCompare(b.date);
        // }
      }
    ];
  };

  return (
    <div className="Table-wrapper">
      <Table
        locale={{ emptyText: loading ? placeholder : "Нету результатов..." }}
        dataSource={result}
        columns={renderColumns()}
      />
    </div>
  );
};

export default ResultTable;
