import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';

const getDataCellClasses = (key, sort) => ({
  cell: true,
  sorted: sort.key === key,
  [`column-${key}`]: true,
});

export const createDataCellConnector = key => (Component) => {
  const wrappedComponent = ({ sort, result }) => (
    <Component
      className={classNames(getDataCellClasses(key, sort))}
      value={result[key]}
      result={result}
    />
  );

  wrappedComponent.propTypes = {
    sort: PropTypes.object.isRequired,
    result: PropTypes.object.isRequired,
  };

  // Let's use the same naming convention as react-redux here.
  wrappedComponent.WrappedComponent = Component;

  wrappedComponent.cellKey = key;

  return wrappedComponent;
};


export function GenericDataCell({ className, value }) {
  return (
    <td className={className}>
      {value}
    </td>
  );
}

GenericDataCell.propTypes = {
  className: PropTypes.string.isRequired,
  value: PropTypes.any,
};

GenericDataCell.defaultProps = {
  value: null,
};
